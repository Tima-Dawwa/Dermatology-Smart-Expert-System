from experta import *
from ExpertSystem.facts import Symptom, ImageDiagnosis, PatientProfile, Diagnosis, DiseaseInfo
import collections
import collections.abc
collections.Mapping = collections.abc.Mapping


class DermatologyExpertSystem(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.diagnosis = None

    def get_diagnosis(self):
        return self.diagnosis

    # Helper method to gather all symptom names currently declared
    def aggregate_symptoms(self):
        current_symptoms = set()
        for fact in self.facts.values():
            if isinstance(fact, Symptom):
                current_symptoms.add(fact['name'])
        self.declare(Fact(current_symptoms=current_symptoms))

    # ============================
    #      RULES for Atopic Dermatitis
    # ============================

    @Rule(
        DiseaseInfo(name="Atopic Dermatitis",
                    common_symptoms=MATCH.symptoms,
                    triggers=MATCH.triggers,
                    common_locations=MATCH.locations,
                    common_age_range=MATCH.age_range,
                    affected_gender=MATCH.gender)
    )
    def evaluate_atopic_dermatitis(self, symptoms, triggers, locations, age_range, gender):
        self.declare(Fact(considering="Atopic Dermatitis"))
        self.declare(Fact(required_symptoms=set(symptoms["required"])))
        self.declare(Fact(optional_symptoms=set(symptoms["optional"])))
        self.declare(Fact(valid_locations=locations))
        self.declare(Fact(valid_triggers=triggers))
        self.declare(Fact(age_bounds=age_range.split("-")))
        self.declare(Fact(valid_gender=gender))
        print("[Reference] Initial disease facts loaded for Atopic Dermatitis")

    @Rule(
        Fact(considering="Atopic Dermatitis")
    )
    def prepare_symptoms(self):
        self.aggregate_symptoms()

    @Rule(
        Fact(considering="Atopic Dermatitis"),
        Fact(required_symptoms=MATCH.req),
        Fact(current_symptoms=MATCH.curr),
        TEST(lambda req, curr: req.issubset(curr))
    )
    def matched_required_symptoms(self, req, curr):
        print("[Reference] All required symptoms matched.")
        self.declare(Fact(required_match=True))

    @Rule(
        Fact(considering="Atopic Dermatitis"),
        Fact(age_bounds=MATCH.bounds),
        PatientProfile(age=MATCH.age),
        TEST(lambda age, bounds: int(bounds[0]) <= age <= int(bounds[1]))
    )
    def match_age(self, age, bounds):
        print(f"[Reference] Age {age} within range {bounds}.")
        self.declare(Fact(age_match=True))

    @Rule(
        Fact(considering="Atopic Dermatitis"),
        Fact(valid_gender=MATCH.g),
        PatientProfile(gender=MATCH.gender),
        TEST(lambda gender, g: g == "both" or gender == g)
    )
    def match_gender(self, gender, g):
        print(f"[Reference] Gender '{gender}' matches '{g}'.")
        self.declare(Fact(gender_match=True))

    @Rule(
        Fact(considering="Atopic Dermatitis"),
        Fact(valid_locations=MATCH.locs),
        Symptom(location=MATCH.loc),
        TEST(lambda loc, locs: loc in locs)
    )
    def match_location(self, loc, locs):
        print(f"[Reference] Location '{loc}' matches known areas.")
        self.declare(Fact(location_match=True))

    @Rule(
        Fact(considering="Atopic Dermatitis"),
        Fact(valid_triggers=MATCH.trig),
        Symptom(trigger=MATCH.t),
        TEST(lambda t, trig: t in trig)
    )
    def match_trigger(self, t, trig):
        print(f"[Reference] Trigger '{t}' matches.")
        self.declare(Fact(trigger_match=True))

    @Rule(
        Fact(considering="Atopic Dermatitis"),
        ImageDiagnosis(tags=MATCH.tags),
        TEST(lambda tags: any(tag in tags for tag in [
             "redness", "scaling", "dry skin"]))
    )
    def match_image(self, tags):
        print(f"[Reference] Vision tags '{tags}' support Atopic Dermatitis.")
        self.declare(Fact(image_support=True))

    @Rule(
        Fact(considering="Atopic Dermatitis"),
        Fact(required_match=True),
        Fact(age_match=True),
        Fact(gender_match=True),
        Fact(location_match=True),
        Fact(trigger_match=True),
        Fact(image_support=True)
    )
    def confirm_atopic_dermatitis(self):
        print("[Reference] All reasoning conditions met.")
        self.declare(Diagnosis(disease="Atopic Dermatitis"))

    @Rule(Diagnosis(disease=MATCH.disease))
    def print_final_diagnosis(self, disease):
        print(f"[Expert System] Final diagnosis: {disease}")
        self.diagnosis = disease
