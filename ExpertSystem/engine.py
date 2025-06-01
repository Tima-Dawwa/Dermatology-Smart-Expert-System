from experta import KnowledgeEngine, Rule, Fact, MATCH, TEST
from ExpertSystem.facts import Symptom, ImageDiagnosis, PatientProfile, Diagnosis
import collections
import collections.abc
collections.Mapping = collections.abc.Mapping


class DermatologyExpertSystem(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.diagnosis = None

    def get_diagnosis(self):
        return self.diagnosis

    # ============================
    #         RULE PLACEHOLDERS
    # ============================

    # here

    # ============================
    #     FINAL OUTPUT HANDLER
    # ============================

    @Rule(Diagnosis(disease=MATCH.disease))
    def print_final_diagnosis(self, disease):
        print(f"[Expert System] Final diagnosis: {disease}")
