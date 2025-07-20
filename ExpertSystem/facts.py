from experta import *
import collections
import collections.abc

collections.Mapping = collections.abc.Mapping


class Answer(Fact):
    ident = Field(str, mandatory=True)
    text = Field(str, mandatory=True)
    cf = Field(float, default=1.0)


class question(Fact):
    ident = Field(str, mandatory=True)
    text = Field(str, mandatory=True)
    valid = Field(list, mandatory=True)
    Type = Field(str, mandatory=True)


class Symptom(Fact):
    name = Field(str, mandatory=True)
    severity = Field(str, default=None)
    duration = Field(str, default=None)
    location = Field(str, default=None)


class PatientProfile(Fact):
    age = Field(int, default=None)
    gender = Field(str, default=None)
    skin_type = Field(str, default=None)
    known_allergies = Field(list, default=[])
    occupation = Field(str, default=None)


class Diagnosis(Fact):
    disease = Field(str, mandatory=True)
    reasoning = Field(str, default=None)
    cf = Field(float, default=1.0)
    age_boosted = Field(bool, default=False)
    duration_boosted = Field(bool, default=False)
    severity_adjusted = Field(bool, default=False)
    merge_count = Field(int, default=0)


class DiseaseInfo(Fact):
    name = Field(str, mandatory=True)
    common_symptoms = Field(dict, mandatory=True)
    age_min = Field(int, default=0)
    age_max = Field(int, default=120)
    common_locations = Field(list, default=[])
    severity_levels = Field(list, default=[])
    common_duration = Field(str, default=None)
    triggers = Field(list, default=[])
    notes = Field(str, default=None)


class NextQuestion(Fact):
    pass


class Stop(Fact):
    pass
