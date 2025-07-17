import  { createContext, useContext, useState, useCallback } from "react";

const BackendContext = createContext();

export function BackendProvider({ children }) {
  const [sessionId, setSessionId] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [answers, setAnswers] = useState([]);
  const [diagnosis, setDiagnosis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState(null);

  const API_BASE = "http://127.0.0.1:8000/api";

  // Fetch current status/question/diagnosis
  const fetchStatus = useCallback(async (id = sessionId) => {
    if (!id) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/sessions/${id}/status`);
      const data = await res.json();
      setCurrentQuestion(data.current_question);
      setDiagnosis(data.diagnosis);
      setProgress(data.progress);
    } catch (e) {
      setError("Failed to fetch status");
    } finally {
      setLoading(false);
    }
  }, [sessionId]);

  // Create a new session
  const createSession = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/sessions`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({}),
      });
      const data = await res.json();
      setSessionId(data.session_id);
      setAnswers([]);
      setDiagnosis(null);
      setProgress(0);
      // Immediately fetch first question
      await fetchStatus(data.session_id);
    } catch (e) {
      setError("Failed to create session");
    } finally {
      setLoading(false);
    }
  }, [fetchStatus]);

  // Submit answer
  const submitAnswer = useCallback(async (answer) => {
    if (!sessionId || !currentQuestion) return;
    setLoading(true);
    setError(null);
    try {
      await fetch(`${API_BASE}/sessions/${sessionId}/answer`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question_id: currentQuestion.question_id,
          answer: answer,
          is_multiple: currentQuestion.is_multiple_choice || false,
        }),
      });
      setAnswers((prev) => [...prev, { question: currentQuestion, answer }]);
      await fetchStatus();
    } catch (e) {
      setError("Failed to submit answer");
    } finally {
      setLoading(false);
    }
  }, [sessionId, currentQuestion, fetchStatus]);

  // Reset/delete session
  const resetSession = useCallback(async () => {
    if (sessionId) {
      try {
        await fetch(`${API_BASE}/sessions/${sessionId}`, { method: "DELETE" });
      } catch {}
    }
    setSessionId(null);
    setCurrentQuestion(null);
    setAnswers([]);
    setDiagnosis(null);
    setProgress(0);
    setError(null);
  }, [sessionId]);

  return (
    <BackendContext.Provider
      value={{
        sessionId,
        currentQuestion,
        answers,
        diagnosis,
        loading,
        progress,
        error,
        createSession,
        fetchStatus,
        submitAnswer,
        resetSession,
      }}
    >
      {children}
    </BackendContext.Provider>
  );
}

export function useBackend() {
  return useContext(BackendContext);
} 