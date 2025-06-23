# ExpertSystem/engine.py

import logging  # --- ENSURE THIS IMPORT IS AT THE TOP ---

from experta import *
from ExpertSystem.facts import Answer, NextQuestion, Stop, Diagnosis
from ExpertSystem.Data.disease import diseases, create_disease_lookup, DURATION_MAPPING
from ExpertSystem.Questions.question import get_question_by_ident

# Create the lookup dictionary once when the module is loaded
disease_info_lookup = create_disease_lookup()


class DermatologyExpert(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.best_diagnosis = None
        self.fired_rules_log = []  # To store print output for GUI display

    @DefFacts()
    def _initial_action(self):
        """Initial facts to start the engine."""
        yield Fact(start=True)

    @Rule(NextQuestion(ident=MATCH.ident), NOT(Answer(ident=MATCH.ident)), salience=200)
    def ask_question_for_gui(self, ident):
        """
        This rule asserts a NextQuestion fact for the GUI to pick up.
        It then halts the engine to allow GUI to get user input.
        """
        self.halt()

    def combine_cf(self, cf1, cf2):
        """Combine confidence factors using standard CF algebra."""
        if cf1 >= 0 and cf2 >= 0:
            return cf1 + cf2 * (1 - cf1)
        elif cf1 < 0 and cf2 < 0:
            return cf1 + cf2 * (1 + cf1)
        else:
            denominator = (1 - min(abs(cf1), abs(cf2)))
            return (cf1 + cf2) / denominator if denominator != 0 else (cf1 + cf2)

    def declare_or_update_diagnosis(self, disease, reasoning, new_cf):
        """
        Declares a new diagnosis or updates an existing one, automatically
        adjusting the CF based on the patient's age, symptom duration, and severity.
        Collects debug output for GUI display.
        """
        log_message = f"\n🔍 PROCESSING DIAGNOSIS: {disease}\n"
        log_message += f"   📋 Rule Evidence: {reasoning}\n"
        log_message += f"   🎯 Base CF from rule: {new_cf:.3f}\n"

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
                        log_message += f"   ✅ Age match bonus: {old_cf:.3f} + 0.15 = {final_new_cf:.3f}\n"
                    else:
                        old_cf = final_new_cf
                        final_new_cf = self.combine_cf(final_new_cf, -0.2)
                        log_message += f"   ❌ Age mismatch penalty: {old_cf:.3f} - 0.2 = {final_new_cf:.3f}\n"
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
                log_message += f"   ⏰ Duration mismatch penalty: {old_cf:.3f} - 0.4 = {final_new_cf:.3f}\n"
            elif disease_duration in DURATION_MAPPING.get(user_duration_text, []):
                old_cf = final_new_cf
                final_new_cf = self.combine_cf(final_new_cf, 0.1)
                log_message += f"   ⏰ Duration match bonus: {old_cf:.3f} + 0.1 = {final_new_cf:.3f}\n"

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
                    log_message += f"   💪 Severity match bonus: {old_cf:.3f} + 0.15 = {final_new_cf:.3f}\n"
                else:
                    old_cf = final_new_cf
                    final_new_cf = self.combine_cf(final_new_cf, -0.15)
                    log_message += f"   💪 Severity mismatch penalty: {old_cf:.3f} - 0.15 = {final_new_cf:.3f}\n"

        # --- Update the diagnosis fact ---
        existing_diagnosis = next((f for f in self.facts.values() if isinstance(
            f, Diagnosis) and f.get("disease") == disease), None)

        if existing_diagnosis:
            log_message += f"\n🔄 COMBINING WITH EXISTING DIAGNOSIS:\n"
            log_message += f"   📊 Existing CF: {existing_diagnosis['cf']:.3f}\n"
            log_message += f"   📊 New CF: {final_new_cf:.3f}\n"

            combined_cf = self.combine_cf(
                existing_diagnosis["cf"], final_new_cf)

            log_message += f"   🎯 COMBINED CF: {combined_cf:.3f}\n"
            log_message += f"   📐 CF Formula: combine_cf({existing_diagnosis['cf']:.3f}, {final_new_cf:.3f}) = {combined_cf:.3f}\n"

            updated_reasoning = f"{existing_diagnosis.get('reasoning', '')}; {reasoning}"
            self.retract(existing_diagnosis)
            self.declare(Diagnosis(disease=disease,
                                   reasoning=updated_reasoning, cf=combined_cf))

            log_message += f"   📝 Updated reasoning: {updated_reasoning}\n"
        else:
            log_message += f"   ✨ NEW DIAGNOSIS CREATED with CF: {final_new_cf:.3f}\n"
            self.declare(Diagnosis(disease=disease,
                                   reasoning=reasoning, cf=final_new_cf))

        log_message += "   " + "─"*50 + "\n"
        self.fired_rules_log.append(log_message)

    @Rule(NOT(NextQuestion(W())), NOT(Fact(id='results_processed')), salience=-1000)
    def process_final_results(self):
        """
        Fires when no more questions are left. Finds the best diagnosis
        and sets self.best_diagnosis. Halts the engine.
        """
        self.declare(Fact(id='results_processed'))
        all_diagnoses = [
            f for f in self.facts.values() if isinstance(f, Diagnosis)]

        if all_diagnoses:
            self.best_diagnosis = max(all_diagnoses, key=lambda d: d['cf'])
        else:
            self.best_diagnosis = None
        self.halt()
