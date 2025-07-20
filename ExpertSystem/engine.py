from experta import *
from ExpertSystem.facts import Answer, DiseaseInfo, NextQuestion, Stop, Diagnosis
from ExpertSystem.Data.disease import diseases, create_disease_lookup, DURATION_MAPPING

disease_info_lookup = create_disease_lookup()


class DermatologyExpert(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.best_diagnosis = None
        self.fired_rules_log = []

    @DefFacts()
    def _initial_action(self):
        yield Fact(start=True)
        for d in diseases:
            yield DiseaseInfo(
                name=d["name"],
                common_symptoms=d.get("common_symptoms", {}),
                age_min=d.get("age_min", 0),
                age_max=d.get("age_max", 120),
                common_locations=d.get("common_locations", []),
                severity_levels=d.get("severity_levels", []),
                common_duration=d.get("common_duration", None),
                triggers=d.get("triggers", []),
                notes=d.get("notes", None),
            )

    @Rule(NextQuestion(ident=MATCH.ident), NOT(Answer(ident=MATCH.ident)), salience=200)
    def ask_question_for_gui(self):
        self.halt()

    def combine_cf(self, cf1, cf2):
        if cf1 >= 0 and cf2 >= 0:
            return cf1 + cf2 * (1 - cf1)
        elif cf1 < 0 and cf2 < 0:
            return cf1 + cf2 * (1 + cf1)
        else:
            denominator = 1 - min(abs(cf1), abs(cf2))
            return (cf1 + cf2) / denominator if denominator != 0 else (cf1 + cf2)

    def merge_reasonings(old_reasoning, new_reason):
        if not old_reasoning:
            return new_reason
        reasoning_parts = set(r.strip() for r in old_reasoning.split(";") if r.strip())
        if new_reason not in reasoning_parts:
            reasoning_parts.add(new_reason)
        return "; ".join(sorted(reasoning_parts))

    @Rule(
        AS.diagnosis
        << Diagnosis(
            disease=MATCH.disease,
            cf=MATCH.old_cf,
            reasoning=MATCH.old_reasoning,
            age_boosted=False,
        ),
        DiseaseInfo(name=MATCH.disease, age_min=MATCH.age_min, age_max=MATCH.age_max),
        Answer(ident="age", text=MATCH.age_str),
        TEST(lambda age_str, age_min, age_max: age_min <= int(age_str) <= age_max),
        salience=50,
    )
    def age_match_bonus(
        self, diagnosis, disease, old_cf, old_reasoning, age_str, age_min, age_max
    ):
        new_cf = self.combine_cf(old_cf, 0.15)
        new_reasoning = (
            f"{old_reasoning}; age match bonus ({age_str} in {age_min}-{age_max})"
        )
        log_message = (
            f"✅ Age match bonus for {disease}: {old_cf:.3f} + 0.15 = {new_cf:.3f}"
        )
        self.fired_rules_log.append(log_message)
        self.retract(diagnosis)
        self.declare(
            Diagnosis(
                disease=disease, cf=new_cf, reasoning=new_reasoning, age_boosted=True
            )
        )

    @Rule(
        AS.diagnosis
        << Diagnosis(
            disease=MATCH.disease,
            cf=MATCH.old_cf,
            reasoning=MATCH.old_reasoning,
            age_boosted=False,
        ),
        DiseaseInfo(name=MATCH.disease, age_min=MATCH.age_min, age_max=MATCH.age_max),
        Answer(ident="age", text=MATCH.age_str),
        TEST(
            lambda age_str, age_min, age_max: not (age_min <= int(age_str) <= age_max)
        ),
        salience=50,
    )
    def age_mismatch_penalty(
        self, diagnosis, disease, old_cf, old_reasoning, age_str, age_min, age_max
    ):
        new_cf = self.combine_cf(old_cf, -0.2)
        new_reasoning = f"{old_reasoning}; age mismatch penalty ({age_str} not in {age_min}-{age_max})"
        log_message = (
            f"❌ Age mismatch penalty for {disease}: {old_cf:.3f} - 0.2 = {new_cf:.3f}"
        )
        self.fired_rules_log.append(log_message)
        self.retract(diagnosis)
        self.declare(
            Diagnosis(
                disease=disease, cf=new_cf, reasoning=new_reasoning, age_boosted=True
            )
        )

    @Rule(
        AS.diagnosis
        << Diagnosis(
            disease=MATCH.disease,
            cf=MATCH.old_cf,
            reasoning=MATCH.old_reasoning,
            age_boosted=True,
            duration_boosted=False,
        ),
        DiseaseInfo(name=MATCH.disease, common_duration=MATCH.disease_duration),
        Answer(ident="duration", text=MATCH.user_duration),
        TEST(
            lambda user_duration, disease_duration: disease_duration
            not in DURATION_MAPPING.get(user_duration, [])
        ),
        salience=45,
    )
    def duration_mismatch_penalty(
        self, diagnosis, disease, old_cf, old_reasoning, user_duration, disease_duration
    ):
        new_cf = self.combine_cf(old_cf, -0.4)
        new_reasoning = f"{old_reasoning}; duration mismatch penalty ({user_duration} vs {disease_duration})"
        log_message = f"⏰ Duration mismatch penalty for {disease}: {old_cf:.3f} - 0.4 = {new_cf:.3f}"
        self.fired_rules_log.append(log_message)
        self.retract(diagnosis)
        self.declare(
            Diagnosis(
                disease=disease,
                cf=new_cf,
                reasoning=new_reasoning,
                age_boosted=True,
                duration_boosted=True,
            )
        )

    @Rule(
        AS.diagnosis
        << Diagnosis(
            disease=MATCH.disease,
            cf=MATCH.old_cf,
            reasoning=MATCH.old_reasoning,
            age_boosted=True,
            duration_boosted=False,
        ),
        DiseaseInfo(name=MATCH.disease, common_duration=MATCH.disease_duration),
        Answer(ident="duration", text=MATCH.user_duration),
        TEST(
            lambda user_duration, disease_duration: disease_duration
            in DURATION_MAPPING.get(user_duration, [])
        ),
        salience=45,
    )
    def duration_match_bonus(
        self, diagnosis, disease, old_cf, old_reasoning, user_duration, disease_duration
    ):
        new_cf = self.combine_cf(old_cf, 0.1)
        new_reasoning = f"{old_reasoning}; duration match bonus ({user_duration} matches {disease_duration})"
        log_message = (
            f"⏰ Duration match bonus for {disease}: {old_cf:.3f} + 0.1 = {new_cf:.3f}"
        )
        self.fired_rules_log.append(log_message)
        self.retract(diagnosis)
        self.declare(
            Diagnosis(
                disease=disease,
                cf=new_cf,
                reasoning=new_reasoning,
                age_boosted=True,
                duration_boosted=True,
            )
        )

    @Rule(
        AS.diagnosis
        << Diagnosis(
            disease=MATCH.disease,
            cf=MATCH.old_cf,
            reasoning=MATCH.old_reasoning,
            age_boosted=True,
            duration_boosted=True,
            severity_adjusted=False,
        ),
        DiseaseInfo(name=MATCH.disease, severity_levels=MATCH.disease_severity_levels),
        Answer(ident="severity", text=MATCH.user_severity),
        TEST(
            lambda user_severity, disease_severity_levels: disease_severity_levels
            and user_severity in disease_severity_levels
        ),
        salience=40,
    )
    def severity_match_bonus(
        self,
        diagnosis,
        disease,
        old_cf,
        old_reasoning,
        user_severity,
        disease_severity_levels,
    ):
        new_cf = self.combine_cf(old_cf, 0.15)
        new_reasoning = f"{old_reasoning}; severity match bonus ({user_severity} in {disease_severity_levels})"
        log_message = (
            f"💪 Severity match bonus for {disease}: {old_cf:.3f} + 0.15 = {new_cf:.3f}"
        )
        self.fired_rules_log.append(log_message)
        self.retract(diagnosis)
        self.declare(
            Diagnosis(
                disease=disease,
                cf=new_cf,
                reasoning=new_reasoning,
                age_boosted=True,
                duration_boosted=True,
                severity_adjusted=True,
            )
        )

    @Rule(
        AS.diagnosis
        << Diagnosis(
            disease=MATCH.disease,
            cf=MATCH.old_cf,
            reasoning=MATCH.old_reasoning,
            age_boosted=True,
            severity_adjusted=False,
        ),
        DiseaseInfo(name=MATCH.disease, severity_levels=MATCH.disease_severity_levels),
        Answer(ident="severity", text=MATCH.user_severity),
        TEST(
            lambda user_severity, disease_severity_levels: disease_severity_levels
            and user_severity not in disease_severity_levels
        ),
        salience=40,
    )
    def severity_mismatch_penalty(
        self,
        diagnosis,
        disease,
        old_cf,
        old_reasoning,
        user_severity,
        disease_severity_levels,
    ):
        new_cf = self.combine_cf(old_cf, -0.15)
        new_reasoning = f"{old_reasoning}; severity mismatch penalty ({user_severity} not in {disease_severity_levels})"
        log_message = f"💪 Severity mismatch penalty for {disease}: {old_cf:.3f} - 0.15 = {new_cf:.3f}"
        self.fired_rules_log.append(log_message)
        self.retract(diagnosis)
        self.declare(
            Diagnosis(
                disease=disease,
                cf=new_cf,
                reasoning=new_reasoning,
                age_boosted=True,
                duration_boosted=True,
                severity_adjusted=True,
            )
        )

    @Rule(
        AS.old_diag
        << Diagnosis(
            disease=MATCH.disease,
            cf=MATCH.old_cf,
            reasoning=MATCH.old_reasoning,
            merge_count=MATCH.old_count,
        ),
        AS.new_diag
        << Diagnosis(
            disease=MATCH.disease,
            cf=MATCH.new_cf,
            reasoning=MATCH.new_reasoning,
            merge_count=MATCH.new_count,
        ),
        TEST(lambda old_diag, new_diag: old_diag != new_diag),
    )
    def combine_duplicate_diagnosis(
        self,
        old_diag,
        new_diag,
        disease,
        old_cf,
        new_cf,
        old_reasoning,
        new_reasoning,
        old_count,
        new_count,
    ):
        combined_cf = self.combine_cf(old_cf, new_cf)
        combined_reasoning = f"{old_reasoning}; {new_reasoning}"
        new_merge_count = max(old_count, new_count) + 1
        log_message = f"🔄 Combining Diagnosis for {disease}: {old_cf:.3f} + {new_cf:.3f} = {combined_cf:.3f} (merge count {new_merge_count})"
        self.fired_rules_log.append(log_message)
        self.retract(old_diag)
        self.retract(new_diag)
        self.declare(
            Diagnosis(
                disease=disease,
                cf=combined_cf,
                reasoning=combined_reasoning,
                merge_count=new_merge_count,
            )
        )

    @Rule(NOT(NextQuestion(W())), NOT(Fact(id="results_processed")), salience=-1000)
    def process_final_results(self):
        self.declare(Fact(id="results_processed"))
        all_diagnoses = [f for f in self.facts.values() if isinstance(f, Diagnosis)]
        if all_diagnoses:
            self.best_diagnosis = max(all_diagnoses, key=lambda d: d["cf"])
        else:
            self.best_diagnosis = None
        self.halt()
