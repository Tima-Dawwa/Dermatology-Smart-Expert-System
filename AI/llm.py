import time
from typing import Dict
from dataclasses import dataclass

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch


@dataclass
class DiagnosisResult:
    """Structure to hold diagnosis results from the expert system"""
    disease: str
    confidence: float
    reasoning: str
    patient_answers: Dict[str, str]


@dataclass
class MedicalExplanation:
    """Structure to hold the medical explanation response from LLM"""
    diagnosis: str
    confidence: float
    detailed_explanation: str
    causes: str
    symptoms_analysis: str
    treatment_recommendations: str
    prognosis: str
    when_to_seek_help: str


class MedicalLLM:
    """Simplified Medical LLM interface using Hugging Face Transformers"""

    def __init__(self, model_name: str = "microsoft/DialoGPT-medium"):
        """
        Initialize the Medical LLM interface
        
        Args:
            model_name: Hugging Face model name/path
        """
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipeline = None

    def test_connection(self) -> bool:
        """Test if the LLM connection is working"""
        try:
            return self.load_model()
        except Exception as e:
            print(f"❌ LLM connection test failed: {str(e)}")
            return False

    def load_model(self) -> bool:
        """Load the model and create pipeline"""
        try:
            print(f"🔄 Loading model: {self.model_name}")
            print(f"📱 Using device: {self.device}")

            # Create pipeline directly - simpler approach
            self.pipeline = pipeline(
                "text-generation",
                model=self.model_name,
                device=0 if self.device == "cuda" else -1,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            )

            print("✅ Model loaded successfully!")
            return True

        except Exception as e:
            print(f"❌ Failed to load model: {str(e)}")
            return False

    def create_medical_prompt(self, diagnosis_result: DiagnosisResult) -> str:
        """Create a medical prompt for explanation"""

        # Build symptom context
        symptoms_list = []
        for key, value in diagnosis_result.patient_answers.items():
            if value not in ['no', 'none', '']:
                formatted_key = key.replace('_', ' ').title()
                symptoms_list.append(f"- {formatted_key}: {value}")

        symptoms_context = "\n".join(
            symptoms_list) if symptoms_list else "No specific symptoms recorded"

        prompt = f"""Medical Case Analysis:

Diagnosis: {diagnosis_result.disease}
Confidence: {diagnosis_result.confidence:.1f}%
Reasoning: {diagnosis_result.reasoning}

Patient Information:
{symptoms_context}

Please respond directly to the patient. Use calm, respectful, and professional language. Clearly explain:

1. **What is this condition?** — Describe it in simple terms.
2. **What causes it?** — List common causes and triggers.
3. **How do the symptoms match the diagnosis?** — Explain how the reported symptoms fit.
4. **What treatments are recommended?** — Share safe, up-to-date treatments (lifestyle or medical).
5. **What is the prognosis?** — What to expect in the short and long term.
6. **When should I seek medical help?** — Describe any warning signs to watch for.

Medical Explanation:"""

        return prompt

    def get_explanation(self, diagnosis_result: DiagnosisResult) -> MedicalExplanation:
        """Get comprehensive medical explanation from the LLM"""

        if not self.pipeline and not self.load_model():
            return self._create_error_explanation(diagnosis_result, "Failed to load model")

        prompt = self.create_medical_prompt(diagnosis_result)

        try:
            print("🤖 Generating AI medical explanation...")
            start_time = time.time()

            # Generate response
            response = self.pipeline(
                prompt,
                max_length=len(prompt.split()) + 512,  # Reasonable max length
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.pipeline.tokenizer.eos_token_id,
                truncation=True
            )

            # Extract generated text (remove input prompt)
            full_response = response[0]['generated_text']
            explanation_text = full_response[len(prompt):].strip()

            response_time = time.time() - start_time
            print(f"✅ AI explanation generated in {response_time:.1f} seconds")

            return self._parse_explanation(explanation_text, diagnosis_result)

        except Exception as e:
            print(f"❌ Error generating explanation: {str(e)}")
            return self._create_error_explanation(diagnosis_result, str(e))

    def _parse_explanation(self, explanation_text: str, diagnosis_result: DiagnosisResult) -> MedicalExplanation:
        """Parse the AI explanation into structured format"""

        sections = {
            'detailed_explanation': '',
            'causes': '',
            'symptoms_analysis': '',
            'treatment_recommendations': '',
            'prognosis': '',
            'when_to_seek_help': ''
        }

        # If explanation is short, put it all in detailed_explanation
        if len(explanation_text) < 200:
            sections['detailed_explanation'] = explanation_text
        else:
            # Try to parse sections
            lines = explanation_text.split('\n')
            current_section = 'detailed_explanation'

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                lower_line = line.lower()

                # Simple section detection
                if 'cause' in lower_line:
                    current_section = 'causes'
                elif 'symptom' in lower_line:
                    current_section = 'symptoms_analysis'
                elif 'treatment' in lower_line:
                    current_section = 'treatment_recommendations'
                elif 'outcome' in lower_line or 'prognosis' in lower_line:
                    current_section = 'prognosis'
                elif 'seek' in lower_line or 'emergency' in lower_line:
                    current_section = 'when_to_seek_help'
                else:
                    if sections[current_section]:
                        sections[current_section] += '\n'
                    sections[current_section] += line

        return MedicalExplanation(
            diagnosis=diagnosis_result.disease,
            confidence=diagnosis_result.confidence,
            detailed_explanation=sections['detailed_explanation'] or explanation_text,
            causes=sections['causes'] or "Not specified",
            symptoms_analysis=sections['symptoms_analysis'] or "Not specified",
            treatment_recommendations=sections['treatment_recommendations'] or "Consult healthcare professional",
            prognosis=sections['prognosis'] or "Not specified",
            when_to_seek_help=sections['when_to_seek_help'] or "Consult if symptoms worsen"
        )

    def _create_error_explanation(self, diagnosis_result: DiagnosisResult, error_msg: str) -> MedicalExplanation:
        """Create a basic explanation when AI fails"""

        basic_explanation = f"""
Based on the analysis, the diagnosis is {diagnosis_result.disease} 
with {diagnosis_result.confidence:.1f}% confidence.

Reasoning: {diagnosis_result.reasoning}

AI explanation unavailable: {error_msg}
Please consult a healthcare professional for detailed information.
        """

        return MedicalExplanation(
            diagnosis=diagnosis_result.disease,
            confidence=diagnosis_result.confidence,
            detailed_explanation=basic_explanation,
            causes="Consult healthcare professional",
            symptoms_analysis="Consult healthcare professional",
            treatment_recommendations="Consult healthcare professional",
            prognosis="Consult healthcare professional",
            when_to_seek_help="Consult healthcare professional"
        )


def process_diagnosis_with_llm(diagnosis_result: DiagnosisResult, llm_instance: MedicalLLM = None) -> MedicalExplanation:
    """
    Process a diagnosis result with LLM to get detailed explanation
    
    Args:
        diagnosis_result: The diagnosis result from expert system
        llm_instance: Optional LLM instance to use
        
    Returns:
        MedicalExplanation with detailed information
    """
    if llm_instance is None:
        llm_instance = MedicalLLM()

    try:
        explanation = llm_instance.get_explanation(diagnosis_result)
        return explanation
    except Exception as e:
        print(f"❌ Error processing diagnosis with LLM: {str(e)}")
        return llm_instance._create_error_explanation(diagnosis_result, str(e))


def display_medical_explanation(explanation: MedicalExplanation):
    """Display the medical explanation"""

    print("\n" + "="*60)
    print("🤖 AI MEDICAL EXPLANATION")
    print("="*60)

    print(f"\n📋 DIAGNOSIS: {explanation.diagnosis}")
    print(f"🎯 CONFIDENCE: {explanation.confidence:.1f}%")

    print(f"\n📝 EXPLANATION:")
    print(explanation.detailed_explanation)

    if explanation.causes != "Not specified":
        print(f"\n🔍 CAUSES:")
        print(explanation.causes)

    if explanation.treatment_recommendations != "Consult healthcare professional":
        print(f"\n💊 TREATMENT:")
        print(explanation.treatment_recommendations)

    print(f"\n🚨 WHEN TO SEEK HELP:")
    print(explanation.when_to_seek_help)

    print("\n" + "="*60)
    print("⚠️  DISCLAIMER: For informational purposes only.")
    print("Always consult qualified healthcare professionals.")
    print("="*60)


if __name__ == "__main__":
    sample_diagnosis = DiagnosisResult(
        disease="Eczema",
        confidence=85.5,
        reasoning="Itchy, dry skin patches with chronic duration",
        patient_answers={
            'age': '25',
            'duration': 'months',
            'severity': 'moderate',
            'itching': 'yes',
            'dry_skin': 'yes'
        }
    )

    llm = MedicalLLM()
    explanation = llm.get_explanation(sample_diagnosis)
    display_medical_explanation(explanation)
