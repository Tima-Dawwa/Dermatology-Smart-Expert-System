from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import uuid
import json
from datetime import datetime
import asyncio
from contextlib import asynccontextmanager

# Import your existing expert system components
from ExpertSystem.engine import DermatologyExpert
from ExpertSystem.Questions.question_flow import apply_question_flow
from ExpertSystem.Questions.diagnosis import apply_diagnostic_rules
from ExpertSystem.facts import Answer, NextQuestion
from ExpertSystem.Questions.question import get_question_by_ident
from AI.llm import explain_result_with_llm
from experta import Fact

# Pydantic models for API


class SessionCreate(BaseModel):
    user_id: Optional[str] = None


class AnswerSubmission(BaseModel):
    question_id: str
    answer: str
    is_multiple: bool = False


class SessionResponse(BaseModel):
    session_id: str
    status: str
    message: str


class QuestionResponse(BaseModel):
    question_id: str
    question_text: str
    question_type: str
    valid_responses: List[str]
    is_multiple_choice: bool
    session_id: str


class DiagnosisResponse(BaseModel):
    session_id: str
    diagnosis: Optional[Dict[str, Any]]
    explanation: Optional[str]
    confidence: Optional[float]
    reasoning: Optional[str]
    completed: bool


class SessionStatus(BaseModel):
    session_id: str
    status: str
    current_question: Optional[QuestionResponse]
    diagnosis: Optional[DiagnosisResponse]
    progress: float


# In-memory session storage (use Redis/database in production)
active_sessions: Dict[str, Dict] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting Dermatology Expert System API...")
    yield
    # Shutdown
    print("Shutting down...")

app = FastAPI(
    title="Dermatology Expert System API",
    description="AI-powered dermatology diagnosis system",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
                   "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_expert_system():
    """Create and configure the expert system with all rules"""
    DermatologyExpertWithLogic = apply_question_flow(DermatologyExpert)
    DermatologyExpertWithLogic = apply_diagnostic_rules(
        DermatologyExpertWithLogic)
    return DermatologyExpertWithLogic()


def run_expert_system(session_id: str):
    """Run the expert system for a session"""
    try:
        session = active_sessions.get(session_id)
        if not session:
            return

        expert_system = session['expert_system']
        expert_system.run()

        # Update session status
        session['status'] = 'processed'
        session['last_updated'] = datetime.now()

    except Exception as e:
        if session_id in active_sessions:
            active_sessions[session_id]['status'] = 'error'
            active_sessions[session_id]['error'] = str(e)


@app.post("/api/sessions", response_model=SessionResponse)
async def create_session(session_data: SessionCreate):
    """Create a new diagnosis session"""
    try:
        session_id = str(uuid.uuid4())
        expert_system = create_expert_system()
        expert_system.reset()

        # Initialize session
        active_sessions[session_id] = {
            'session_id': session_id,
            'user_id': session_data.user_id,
            'expert_system': expert_system,
            'status': 'initialized',
            'created_at': datetime.now(),
            'last_updated': datetime.now(),
            'answers': {},
            'current_question': None,
            'diagnosis': None
        }

        # Start the expert system
        expert_system.declare(Fact(start=True))
        run_expert_system(session_id)

        return SessionResponse(
            session_id=session_id,
            status="created",
            message="Session created successfully"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error creating session: {str(e)}")


@app.get("/api/sessions/{session_id}/status", response_model=SessionStatus)
async def get_session_status(session_id: str):
    """Get current session status and next question if available"""
    try:
        session = active_sessions.get(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        expert_system = session['expert_system']

        # Check for next question
        next_question_fact = next(
            (f for f in expert_system.facts.values()
             if isinstance(f, NextQuestion)),
            None
        )

        # Check if diagnosis is complete
        results_processed_fact = next(
            (f for f in expert_system.facts.values()
             if isinstance(f, Fact) and f.get('id') == 'results_processed'),
            None
        )

        current_question = None
        diagnosis = None

        if next_question_fact:
            # Get question details
            question_ident = next_question_fact['ident']
            question_data = get_question_by_ident(question_ident)

            if question_data:
                is_multiple = "Select all that apply" in question_data['text']
                current_question = QuestionResponse(
                    question_id=question_ident,
                    question_text=question_data['text'],
                    question_type=question_data['Type'],
                    valid_responses=question_data['valid'],
                    is_multiple_choice=is_multiple,
                    session_id=session_id
                )
                session['current_question'] = current_question

        elif results_processed_fact:
            # Get diagnosis results
            best_diagnosis = expert_system.best_diagnosis
            if best_diagnosis:
                # Get AI explanation
                result_text = f"Primary Diagnosis: {best_diagnosis.get('disease')}\nConfidence: {best_diagnosis.get('cf', 0.0) * 100:.1f}%\nReasoning: {best_diagnosis.get('reasoning')}"
                explanation = explain_result_with_llm(result_text)

                diagnosis = DiagnosisResponse(
                    session_id=session_id,
                    diagnosis=best_diagnosis,
                    explanation=explanation,
                    confidence=best_diagnosis.get('cf', 0.0) * 100,
                    reasoning=best_diagnosis.get('reasoning'),
                    completed=True
                )
                session['diagnosis'] = diagnosis

        # Calculate progress (rough estimate)
        progress = len(session['answers']) / 10.0 * \
            100  # Assume ~10 questions max
        progress = min(progress, 95.0)  # Cap at 95% until diagnosis complete

        if diagnosis:
            progress = 100.0

        return SessionStatus(
            session_id=session_id,
            status=session['status'],
            current_question=current_question,
            diagnosis=diagnosis,
            progress=progress
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting session status: {str(e)}")


@app.post("/api/sessions/{session_id}/answer")
async def submit_answer(session_id: str, answer_data: AnswerSubmission, background_tasks: BackgroundTasks):
    """Submit an answer to the current question"""
    try:
        session = active_sessions.get(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        expert_system = session['expert_system']

        # Remove the NextQuestion fact for this question
        next_q_fact_id = None
        for fact_id, fact in expert_system.facts.items():
            if isinstance(fact, NextQuestion) and fact['ident'] == answer_data.question_id:
                next_q_fact_id = fact_id
                break

        if next_q_fact_id is not None:
            expert_system.retract(next_q_fact_id)

        # Store answer in session
        session['answers'][answer_data.question_id] = answer_data.answer

        # Declare answer facts
        is_multi_select_question = answer_data.question_id in [
            'locations']  # Add other multi-select questions

        if is_multi_select_question and answer_data.is_multiple:
            # Handle multiple selections
            individual_answers = [
                a.strip() for a in answer_data.answer.split(',') if a.strip()]
            for individual_ans in individual_answers:
                expert_system.declare(
                    Answer(ident=answer_data.question_id, text=individual_ans.lower()))
        else:
            # Handle single answer
            expert_system.declare(
                Answer(ident=answer_data.question_id, text=answer_data.answer.lower()))

        # Update session
        session['last_updated'] = datetime.now()
        session['status'] = 'processing'

        # Run expert system in background
        background_tasks.add_task(run_expert_system, session_id)

        return {"message": "Answer submitted successfully", "session_id": session_id}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error submitting answer: {str(e)}")


@app.get("/api/sessions/{session_id}/diagnosis", response_model=DiagnosisResponse)
async def get_diagnosis(session_id: str):
    """Get the final diagnosis for a session"""
    try:
        session = active_sessions.get(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        if session.get('diagnosis'):
            return session['diagnosis']
        else:
            return DiagnosisResponse(
                session_id=session_id,
                diagnosis=None,
                explanation=None,
                confidence=None,
                reasoning=None,
                completed=False
            )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting diagnosis: {str(e)}")


@app.delete("/api/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a session"""
    try:
        if session_id in active_sessions:
            del active_sessions[session_id]
            return {"message": "Session deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Session not found")

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error deleting session: {str(e)}")


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "active_sessions": len(active_sessions)
    }

# Error handlers


@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Not found", "detail": str(exc)}


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"error": "Internal server error", "detail": str(exc)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
