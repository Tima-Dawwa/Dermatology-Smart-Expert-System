from experta import *
import collections
import collections.abc
collections.Mapping = collections.abc.Mapping

# -- User Answers to Questions --


class Answer(Fact):
    """
    Stores user's response to a specific question, with optional certainty factor.
    """
    ident = Field(
        str, mandatory=True)     # Unique ID of the question (e.g., 'itching')
    # User response (e.g., 'yes', '2 weeks')
    text = Field(str, mandatory=True)
    cf = Field(float, default=1.0)         # Certainty Factor (0 to 1)

# -- Questions to be asked --


class question(Fact):
    """
    Represents a question asked to the user.
    """
    ident = Field(str, mandatory=True)     # ID for internal rule logic
    # Displayed text (e.g., "Do you have itching?")
    text = Field(str, mandatory=True)
    # Allowed answers (['yes', 'no'], etc.)
    valid = Field(list, mandatory=True)
    Type = Field(str, mandatory=True)      # 'multi', 'number', or 'text'

# -- Symptom: Manually entered or extracted by questions --


class Symptom(Fact):
    """
    A symptom observed or reported by the patient.
    """
    name = Field(str, mandatory=True)      # e.g., 'itching', 'redness'
    severity = Field(str, default=None)    # e.g., 'mild', 'moderate', 'severe'
    duration = Field(str, default=None)    # e.g., '2 weeks'
    location = Field(str, default=None)    # e.g., 'scalp', 'face', 'arms'

# -- Computer Vision-Based Diagnosis --


class ImageDiagnosis(Fact):
    """
    A disease predicted by the vision model.
    """
    disease = Field(str, mandatory=True)        # e.g., 'Psoriasis'
    confidence = Field(float, mandatory=True)   # e.g., 0.85

# -- Basic Patient Metadata --


class PatientProfile(Fact):
    """
    Basic patient information to support personalized diagnosis.
    """
    age = Field(int, default=None)
    gender = Field(str, default=None)           # e.g., 'male', 'female'
    skin_type = Field(str, default=None)        # e.g., 'oily', 'dry'
    known_allergies = Field(list, default=[])   # e.g., ['pollen', 'milk']
    occupation = Field(str, default=None)       # e.g., 'construction worker'

# -- Final System Diagnosis --


class Diagnosis(Fact):
    """
    Final diagnosis by the expert system.
    """
    disease = Field(str, mandatory=True)        # e.g., 'Eczema'
    reasoning = Field(str, default=None)        # Explanation
    cf = Field(float, default=1.0)              # Overall confidence

# -- Disease Metadata (Knowledge base fact) --


class DiseaseInfo(Fact):
    """
    Metadata about a disease — optional layer for knowledge rules.
    """
    name = Field(str, mandatory=True)
    common_symptoms = Field(dict, mandatory=True)
    common_age_range = Field(str, default=None)         # e.g., '20-40'
    common_locations = Field(list, default=[])
    severity_levels = Field(list, default=[])
    common_duration = Field(str, default=None)          # e.g., '2 weeks'
    triggers = Field(list, default=[])                  # e.g., ['stress']
    # common_treatments = Field(list, default=[])
    notes = Field(str, default=None)                    # Extra notes


class NextQuestion(Fact):
    """Represents the next question to be asked."""
    pass


class Stop(Fact):
    """A flag to stop the engine once a diagnosis is made."""
    pass
