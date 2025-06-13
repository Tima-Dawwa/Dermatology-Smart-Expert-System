from ExpertSystem.facts import *
# Correctly import the data and the new lookup function
from ExpertSystem.Data.disease import diseases, create_disease_lookup, DURATION_MAPPING
from ExpertSystem.Questions.question import get_question_by_ident
from experta import *

# Create the lookup dictionary once when the module is loaded
disease_info_lookup = create_disease_lookup()


class DermatologyExpert(KnowledgeEngine):
    def __init__(self):
        super().__init__()

    @DefFacts()
    def _initial_action(self):
        """Initial facts to start the engine."""
        yield Fact(start=True)
        self.best_diagnosis = None

    def ask_user(self, question_text, valid_responses, question_type):
        """Handles the user interaction (I/O) for both text and numbers."""
        print("\n🧐 " + question_text)

        if question_type == 'number':
            # Loop until a valid number is entered
            while True:
                response = input("Your answer (as a number): ").strip()
                if response.isdigit():
                    return response
                else:
                    print("Invalid input. Please enter a valid number.")
        else:
            # Handle multiple choice questions
            if valid_responses:
                print(f"Valid responses: {', '.join(valid_responses)}")
            while True:
                response = input("Your answer: ").strip().lower()
                if not valid_responses or response in valid_responses:
                    return response
                else:
                    print(
                        f"Invalid response. Please enter one of: {', '.join(valid_responses)}")

    @Rule(NextQuestion(ident=MATCH.ident), NOT(Answer(ident=MATCH.ident)), salience=200)
    def ask_question(self, ident):
        """Generic rule to ask the next question, now handling question types."""
        question = get_question_by_ident(ident)
        question_text = question['text']
        valid_responses = question['valid']
        question_type = question['Type']

        response = self.ask_user(question_text, valid_responses, question_type)
        self.declare(Answer(ident=ident, text=response))

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
        """
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
                        final_new_cf = self.combine_cf(
                            final_new_cf, 0.15)  # Boost for age match
                    else:
                        final_new_cf = self.combine_cf(
                            final_new_cf, -0.2)  # Penalty for age mismatch
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
                # Strong penalty for mismatch
                final_new_cf = self.combine_cf(final_new_cf, -0.4)
            elif disease_duration in DURATION_MAPPING.get(user_duration_text, []):
                final_new_cf = self.combine_cf(
                    final_new_cf, 0.1)  # Small boost for match

        # --- Severity Logic ---
        severity_answer = next((f for f in self.facts.values() if isinstance(
            f, Answer) and f.get("ident") == "severity"), None)
        if severity_answer:
            disease_severity_levels = disease_info.get('severity_levels', [])
            user_severity = severity_answer['text']

            if disease_severity_levels:
                if user_severity in disease_severity_levels:
                    final_new_cf = self.combine_cf(
                        final_new_cf, 0.15)  # Boost for severity match
                else:
                    final_new_cf = self.combine_cf(
                        final_new_cf, -0.15)  # Penalty for mismatch

        # --- Update the diagnosis fact ---
        existing_diagnosis = next((f for f in self.facts.values() if isinstance(
            f, Diagnosis) and f.get("disease") == disease), None)

        if existing_diagnosis:
            combined_cf = self.combine_cf(
                existing_diagnosis["cf"], final_new_cf)
            updated_reasoning = f"{existing_diagnosis.get('reasoning', '')}; {reasoning}"
            self.retract(existing_diagnosis)
            self.declare(Diagnosis(disease=disease,
                         reasoning=updated_reasoning, cf=combined_cf))
        else:
            self.declare(Diagnosis(disease=disease,
                         reasoning=reasoning, cf=final_new_cf))

    @Rule(NOT(NextQuestion(W())), NOT(Fact(id='results_printed')), salience=-1000)
    def display_results(self):
        """
        Fires when no more questions are left. Finds the best diagnosis
        and prints the final report.
        """
        self.declare(Fact(id='results_printed'))
        all_diagnoses = [
            f for f in self.facts.values() if isinstance(f, Diagnosis)]

        if not all_diagnoses:
            self.print_final_diagnoses(None)
            return

        best_diagnosis = max(all_diagnoses, key=lambda d: d['cf'])
        self.best_diagnosis = best_diagnosis
        self.print_final_diagnoses(best_diagnosis)

    def print_final_diagnoses(self, diag):
        """Prints the final, most likely diagnosis or a 'not found' message."""
        print("\n" + "="*50)
        print("🏥 FINAL DIAGNOSTIC RESULTS")
        print("="*50)

        if not diag:
            print("⚠️ No diagnosis could be made based on the provided answers.")
        else:
            print(f"\nMost Likely Diagnosis: {diag['disease']}")
            print(f"   Confidence: {diag['cf'] * 100:.1f}%")
            if diag.get('reasoning'):
                print(f"   Reasoning: {diag['reasoning']}")

        print("\n" + "="*50)
        print("⚠️  DISCLAIMER: This is a preliminary assessment.")
        print(
            "Please consult a healthcare professional for proper diagnosis and treatment.")
        print("="*50)
