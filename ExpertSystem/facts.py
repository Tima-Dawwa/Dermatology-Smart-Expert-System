from experta import *
import collections
import collections.abc
collections.Mapping = collections.abc.Mapping


class Symptom(Fact):
    """
    A symptom observed or reported by the patient.
    Only 'name' is required — other fields are optional and can support more detailed reasoning.
    """
    name = Field(str, mandatory=True)      # e.g., 'itching', 'redness'
    severity = Field(str, default=None)    # e.g., 'mild', 'moderate', 'severe'
    duration = Field(str, default=None)    # e.g., '1 day', '2 weeks'
    location = Field(str, default=None)    # e.g., 'scalp', 'face', 'arms'


class ImageDiagnosis(Fact):
    """
    A disease predicted by the vision model.
    """
    disease = Field(str, mandatory=True)     # e.g., 'Psoriasis'
    confidence = Field(float, mandatory=True)  # Model confidence, e.g., 0.87


class PatientProfile(Fact):
    """
    Basic patient information to support diagnosis.
    """
    age = Field(int, default=None)
    gender = Field(str, default=None)    # 'male' / 'female' /
    skin_type = Field(str, default=None)  # 'oily' / 'dry' / etc
    known_allergies = Field(list, default=[])  # food / milk
    occupation = Field(str)  # work (engineer, construction, doctor)


class Diagnosis(Fact):
    """
    Final diagnosis by the expert system.
    """
    disease = Field(str, mandatory=True)     # e.g., 'Eczema'
    reasoning = Field(str, default=None)  # why this diagnosis was selected


class DiseaseInfo(Fact):
    """A full disease profile loaded from JSON."""
    name = Field(str, mandatory=True)
    # {"required": [...], "optional": [...]}
    common_symptoms = Field(dict, mandatory=True)
    affected_gender = Field(str, mandatory=False)
    common_age_range = Field(str, mandatory=False)
    common_locations = Field(list, mandatory=False)
    severity_levels = Field(list, mandatory=False)
    common_duration = Field(str, mandatory=False)
    triggers = Field(list, mandatory=False)
    common_treatments = Field(list, mandatory=False)
    notes = Field(str, mandatory=False)
