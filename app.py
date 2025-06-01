from ExpertSystem.facts import Symptom, ImageDiagnosis, PatientProfile, DiseaseInfo
from ExpertSystem.engine import DermatologyExpertSystem
import os
import json
import collections
import collections.abc
from experta import *

collections.Mapping = collections.abc.Mapping

json_path = os.path.abspath('Data/diseases.json')

with open(json_path, "r") as f:
    disease_data = json.load(f)

print(type(disease_data))

engine = DermatologyExpertSystem()
engine.reset()

diseases = disease_data["diseases"]
for disease in diseases:
    engine.declare(DiseaseInfo(**disease))

engine.declare(PatientProfile(age=8, gender="female"))
engine.declare(Symptom(name="itching"))
engine.declare(Symptom(name="dry skin"))
engine.declare(Symptom(name="red patches"))
engine.declare(Fact(trigger="weather changes"))
engine.declare(Symptom(name="some symptom", location="elbows"))
symptom_names = {"itching", "dry skin", "red patches"}
symptom_names = set()
for fact in engine.facts.values():
    if isinstance(fact, Symptom):
        symptom_names.add(fact["name"])
engine.declare(Fact(symptoms=symptom_names))

engine.declare(ImageDiagnosis(disease="Atopic Dermatitis", confidence=0.9))
engine.run()
print("Diagnosis result:", engine.get_diagnosis())
