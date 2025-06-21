from experta import *
from ExpertSystem.facts import Answer, NextQuestion, Stop, Diagnosis
from ExpertSystem.Data.disease import diseases, create_disease_lookup, DURATION_MAPPING
from ExpertSystem.Questions.question import get_question_by_ident

from AI.llm import MedicalLLM, DiagnosisResult, process_diagnosis_with_llm, display_medical_explanation

# Create the lookup dictionary once when the module is loaded
disease_info_lookup = create_disease_lookup()


class DermatologyExpert(KnowledgeEngine):
    def __init__(self, use_llm=True, llm_instance=None, model_name="microsoft/DialoGPT-medium"):
        super().__init__()
        self.use_llm = use_llm
        self.llm = llm_instance if llm_instance else (
            MedicalLLM(model_name=model_name) if use_llm else None)
        self.patient_answers = {}  # Store all patient answers for LLM
        self.best_diagnosis = None  # Initialize here for consistency

    @DefFacts()
    def _initial_action(self):
        """Initial facts to start the engine."""
        yield Fact(start=True)

    # RULE MODIFIED: No longer calls self.ask_user directly
    @Rule(NextQuestion(ident=MATCH.ident), NOT(Answer(ident=MATCH.ident)), salience=200)
    # Renamed for clarity that it's for GUI
    def ask_question_for_gui(self, ident):
        """
        This rule asserts a NextQuestion fact for the GUI to pick up.
        It then halts the engine to allow GUI to get user input.
        """
        # The GUI will now read this fact and display the question.
        # No direct user interaction (input()) here.
        # It also implicitly makes sure that a question is declared only if no answer exists for it yet.
        # Halt the engine, signaling to the GUI that it needs to wait for input.
        self.halt()

    def combine_cf(self, cf1, cf2):
        """Combine confidence factors using standard CF algebra."""
        if cf1 >= 0 and cf2 >= 0:
            return cf1 + cf2 * (1 - cf1)
        elif cf1 < 0 and cf2 < 0:
            return cf1 + cf2 * (1 + cf1)
        else:
            return (cf1 + cf2) / (1 - min(abs(cf1), abs(cf2)))

    def declare_or_update_diagnosis(self, disease, reasoning, new_cf):
        """
        Declares a new diagnosis or updates an existing one, automatically
        adjusting the CF based on the patient's age, symptom duration, and severity.
        NOW WITH DEBUG OUTPUT FOR CF COMBINATION
        """
        print(f"\n🔍 PROCESSING DIAGNOSIS: {disease}")
        print(f"   📋 Rule Evidence: {reasoning}")
        print(f"   🎯 Base CF from rule: {new_cf}")

        # --- Base CF ---
        final_new_cf = new_cf
        disease_info = disease_info_lookup.get(disease, {})

        # --- Age Logic ---
        age_answer = next((f for f in self.facts.values() if isinstance(
            f, Answer) and f.get("ident") == "age"), None)
        if age_answer:
            age_min = disease_info.get('age_min')
            age_max = disease_info.get('age_max')
            if age_min is not None and age_max is not None:
                try:
                    user_age = int(age_answer['text'])
                    if age_min <= user_age <= age_max:
                        old_cf = final_new_cf
                        final_new_cf = self.combine_cf(final_new_cf, 0.15)
                        print(
                            f"   ✅ Age match bonus: {old_cf} + 0.15 = {final_new_cf:.3f}")
                    else:
                        old_cf = final_new_cf
                        final_new_cf = self.combine_cf(final_new_cf, -0.2)
                        print(
                            f"   ❌ Age mismatch penalty: {old_cf} - 0.2 = {final_new_cf:.3f}")
                except ValueError:
                    pass

        # --- Duration Logic ---
        duration_answer = next((f for f in self.facts.values() if isinstance(
            f, Answer) and f.get("ident") == "duration"), None)
        if duration_answer:
            disease_duration = disease_info.get('common_duration')
            user_duration_text = duration_answer['text']

            long_term_user_durations = [
                "weeks to months", "months to years", "chronic", "chronic with flares"]
            short_term_disease_durations = [
                "1-2 weeks", "1-3 weeks", "2-4 weeks", "days to weeks"]

            if user_duration_text in long_term_user_durations and disease_duration in short_term_disease_durations:
                old_cf = final_new_cf
                final_new_cf = self.combine_cf(final_new_cf, -0.4)
                print(
                    f"   ⏰ Duration mismatch penalty: {old_cf} - 0.4 = {final_new_cf:.3f}")
            elif disease_duration in DURATION_MAPPING.get(user_duration_text, []):
                old_cf = final_new_cf
                final_new_cf = self.combine_cf(final_new_cf, 0.1)
                print(
                    f"   ⏰ Duration match bonus: {old_cf} + 0.1 = {final_new_cf:.3f}")

        # --- Severity Logic ---
        severity_answer = next((f for f in self.facts.values() if isinstance(
            f, Answer) and f.get("ident") == "severity"), None)
        if severity_answer:
            disease_severity_levels = disease_info.get('severity_levels', [])
            user_severity = severity_answer['text']

            if disease_severity_levels:
                if user_severity in disease_severity_levels:
                    old_cf = final_new_cf
                    final_new_cf = self.combine_cf(final_new_cf, 0.15)
                    print(
                        f"   💪 Severity match bonus: {old_cf} + 0.15 = {final_new_cf:.3f}")
                else:
                    old_cf = final_new_cf
                    final_new_cf = self.combine_cf(final_new_cf, -0.15)
                    print(
                        f"   💪 Severity mismatch penalty: {old_cf} - 0.15 = {final_new_cf:.3f}")

        # --- Update the diagnosis fact ---
        existing_diagnosis = next((f for f in self.facts.values() if isinstance(
            f, Diagnosis) and f.get("disease") == disease), None)

        if existing_diagnosis:
            print(f"\n🔄 COMBINING WITH EXISTING DIAGNOSIS:")
            print(f"   📊 Existing CF: {existing_diagnosis['cf']:.3f}")
            print(f"   📊 New CF: {final_new_cf:.3f}")

            combined_cf = self.combine_cf(
                existing_diagnosis["cf"], final_new_cf)

            print(f"   🎯 COMBINED CF: {combined_cf:.3f}")
            print(
                f"   📐 CF Formula: combine_cf({existing_diagnosis['cf']:.3f}, {final_new_cf:.3f}) = {combined_cf:.3f}")

            updated_reasoning = f"{existing_diagnosis.get('reasoning', '')}; {reasoning}"
            self.retract(existing_diagnosis)
            self.declare(Diagnosis(disease=disease,
                                   reasoning=updated_reasoning, cf=combined_cf))

            print(f"   📝 Updated reasoning: {updated_reasoning}")
        else:
            print(f"   ✨ NEW DIAGNOSIS CREATED with CF: {final_new_cf:.3f}")
            self.declare(Diagnosis(disease=disease,
                                   reasoning=reasoning, cf=final_new_cf))

        print("   " + "─"*50)

    def create_diagnosis_result(self) -> DiagnosisResult:
        """Create a DiagnosisResult object from the current best diagnosis"""
        if not self.best_diagnosis:
            return None

        return DiagnosisResult(
            disease=self.best_diagnosis.get('disease', 'Unknown'),
            confidence=self.best_diagnosis.get('cf', 0) * 100,
            reasoning=self.best_diagnosis.get(
                'reasoning', 'No reasoning available'),
            patient_answers=self.patient_answers
        )

    # RULE MODIFIED: No longer prints directly, just sets best_diagnosis and halts.
    @Rule(NOT(NextQuestion(W())), NOT(Fact(id='results_processed')), salience=-1000)
    def process_final_results(self):  # Renamed for clarity
        """
        Fires when no more questions are left. Finds the best diagnosis
        and sets self.best_diagnosis. Halts the engine.
        """
        self.declare(Fact(id='results_processed')
                     )  # Mark that results have been processed by the engine
        all_diagnoses = [
            f for f in self.facts.values() if isinstance(f, Diagnosis)]

        if all_diagnoses:
            self.best_diagnosis = max(all_diagnoses, key=lambda d: d['cf'])
        else:
            self.best_diagnosis = None  # Explicitly set to None if no diagnosis

        # Halt the engine, signaling to the GUI that the diagnosis process is complete.
        self.halt()

    def get_llm_explanation_only(self):
        """
        Get only the LLM explanation without running the full display.
        Useful for API/CLI modes.
        """
        if not self.use_llm or not self.best_diagnosis or not self.llm:
            return None

        try:
            diagnosis_result = self.create_diagnosis_result()
            return self.llm.get_explanation(diagnosis_result)
        except Exception as e:
            print(f"Error generating LLM explanation: {str(e)}")
            return None
