from experta import Rule, Fact, MATCH, NOT
from ExpertSystem.facts import Answer


def apply_question_flow(cls):
    @Rule(NOT(Answer(ident="age_range")), salience=100)
    def start_with_age(self):
        self.declare(Fact(next="age_range"))
    cls.start_with_age = start_with_age

    # PHASE 1: Demographics and Basic Assessment
    @Rule(Answer(ident="age_range", text=MATCH.response))
    def after_age(self, response):
        self.declare(Fact(next="common_duration"))
    cls.after_age = after_age

    @Rule(Answer(ident="common_duration", text=MATCH.response))
    def after_duration(self, response):
        self.declare(Fact(next="severity_levels"))
    cls.after_duration = after_duration

    @Rule(Answer(ident="severity_levels", text=MATCH.response))
    def after_severity(self, response):
        self.declare(Fact(next="itching"))
    cls.after_severity = after_severity

    # PHASE 2: Primary Symptom Branching
    @Rule(Answer(ident="itching", text="yes"))
    def itching_yes_branch(self):
        self.declare(Fact(next="dryness"))
        self.declare(Fact(branch="itchy_conditions"))
    cls.itching_yes_branch = itching_yes_branch

    @Rule(Answer(ident="itching", text="no"))
    def itching_no_branch(self):
        self.declare(Fact(next="painful_blisters"))
        self.declare(Fact(branch="non_itchy_conditions"))
    cls.itching_no_branch = itching_no_branch

    # ITCHY CONDITIONS BRANCH
    @Rule(Answer(ident="dryness", text="yes"), Fact(branch="itchy_conditions"))
    def dry_itchy_branch(self):
        self.declare(Fact(next="scaling"))
        self.declare(Fact(sub_branch="eczema_psoriasis"))
    cls.dry_itchy_branch = dry_itchy_branch

    @Rule(Answer(ident="dryness", text="no"), Fact(branch="itchy_conditions"))
    def wet_itchy_branch(self):
        self.declare(Fact(next="ring_shaped_rash"))
        self.declare(Fact(sub_branch="fungal_contact"))
    cls.wet_itchy_branch = wet_itchy_branch

    # Eczema/Psoriasis Sub-branch
    @Rule(Answer(ident="scaling", text="yes"), Fact(sub_branch="eczema_psoriasis"))
    def scaling_yes_psoriasis(self):
        self.declare(Fact(next="redness"))
        self.declare(Fact(condition_group="psoriasis_likely"))
    cls.scaling_yes_psoriasis = scaling_yes_psoriasis

    @Rule(Answer(ident="scaling", text="no"), Fact(sub_branch="eczema_psoriasis"))
    def scaling_no_eczema(self):
        self.declare(Fact(next="redness_and_inflammation"))
        self.declare(Fact(condition_group="eczema_likely"))
    cls.scaling_no_eczema = scaling_no_eczema

    # Psoriasis path
    @Rule(Answer(ident="redness", text="yes"), Fact(condition_group="psoriasis_likely"))
    def psoriasis_path(self):
        self.declare(Fact(next="stress"))
    cls.psoriasis_path = psoriasis_path

    @Rule(Answer(ident="stress", text=MATCH.response), Fact(condition_group="psoriasis_likely"))
    def psoriasis_triggers(self, response):
        self.declare(Fact(next="infections"))
    cls.psoriasis_triggers = psoriasis_triggers

    @Rule(Answer(ident="infections", text=MATCH.response), Fact(condition_group="psoriasis_likely"))
    def psoriasis_location(self, response):
        self.declare(Fact(next="psoriasis_locations"))
    cls.psoriasis_location = psoriasis_location

    # Eczema path
    @Rule(Answer(ident="redness_and_inflammation", text="yes"), Fact(condition_group="eczema_likely"))
    def eczema_path(self):
        self.declare(Fact(next="crusting_or_oozing"))
    cls.eczema_path = eczema_path

    @Rule(Answer(ident="crusting_or_oozing", text=MATCH.response), Fact(condition_group="eczema_likely"))
    def eczema_triggers(self, response):
        self.declare(Fact(next="allergens"))
    cls.eczema_triggers = eczema_triggers

    @Rule(Answer(ident="allergens", text=MATCH.response), Fact(condition_group="eczema_likely"))
    def eczema_location(self, response):
        self.declare(Fact(next="eczema_locations"))
    cls.eczema_location = eczema_location

    # Fungal/Contact Sub-branch
    @Rule(Answer(ident="ring_shaped_rash", text="yes"), Fact(sub_branch="fungal_contact"))
    def fungal_path(self):
        self.declare(Fact(next="scaly_skin"))
        self.declare(Fact(condition_group="fungal_likely"))
    cls.fungal_path = fungal_path

    @Rule(Answer(ident="ring_shaped_rash", text="no"), Fact(sub_branch="fungal_contact"))
    def contact_path(self):
        self.declare(Fact(next="rash"))
        self.declare(Fact(condition_group="contact_likely"))
    cls.contact_path = contact_path

    # Fungal infection path
    @Rule(Answer(ident="scaly_skin", text=MATCH.response), Fact(condition_group="fungal_likely"))
    def fungal_environment(self, response):
        self.declare(Fact(next="warm_moist_environments"))
    cls.fungal_environment = fungal_environment

    @Rule(Answer(ident="warm_moist_environments", text=MATCH.response), Fact(condition_group="fungal_likely"))
    def fungal_location(self, response):
        self.declare(Fact(next="fungal_locations"))
    cls.fungal_location = fungal_location

    # Contact dermatitis path
    @Rule(Answer(ident="rash", text="yes"), Fact(condition_group="contact_likely"))
    def contact_blisters(self):
        self.declare(Fact(next="blisters"))
    cls.contact_blisters = contact_blisters

    @Rule(Answer(ident="blisters", text=MATCH.response), Fact(condition_group="contact_likely"))
    def contact_triggers(self, response):
        self.declare(Fact(next="plants"))
    cls.contact_triggers = contact_triggers

    @Rule(Answer(ident="plants", text=MATCH.response), Fact(condition_group="contact_likely"))
    def contact_location(self, response):
        self.declare(Fact(next="contact_locations"))
    cls.contact_location = contact_location

    # NON-ITCHY CONDITIONS BRANCH
    @Rule(Answer(ident="painful_blisters", text="yes"), Fact(branch="non_itchy_conditions"))
    def viral_path(self):
        self.declare(Fact(next="tingling_or_burning_before_rash"))
        self.declare(Fact(condition_group="viral_likely"))
    cls.viral_path = viral_path

    @Rule(Answer(ident="painful_blisters", text="no"), Fact(branch="non_itchy_conditions"))
    def growth_nail_path(self):
        self.declare(Fact(next="soft_lump_under_skin"))
        self.declare(Fact(sub_branch="growths_nails"))
    cls.growth_nail_path = growth_nail_path

    # Viral infection path
    @Rule(Answer(ident="tingling_or_burning_before_rash", text=MATCH.response), Fact(condition_group="viral_likely"))
    def viral_triggers(self, response):
        self.declare(Fact(next="stress"))
    cls.viral_triggers = viral_triggers

    @Rule(Answer(ident="stress", text=MATCH.response), Fact(condition_group="viral_likely"))
    def viral_location(self, response):
        self.declare(Fact(next="viral_locations"))
    cls.viral_location = viral_location

    # Growths/Nails Sub-branch
    @Rule(Answer(ident="soft_lump_under_skin", text="yes"), Fact(sub_branch="growths_nails"))
    def benign_growth_path(self):
        self.declare(Fact(next="slow_growth"))
        self.declare(Fact(condition_group="benign_likely"))
    cls.benign_growth_path = benign_growth_path

    @Rule(Answer(ident="soft_lump_under_skin", text="no"), Fact(sub_branch="growths_nails"))
    def nail_or_serious_path(self):
        self.declare(Fact(next="thickened_nails"))
        self.declare(Fact(sub_branch="nails_serious"))
    cls.nail_or_serious_path = nail_or_serious_path

    # Benign growth path
    @Rule(Answer(ident="slow_growth", text=MATCH.response), Fact(condition_group="benign_likely"))
    def benign_age_check(self, response):
        self.declare(Fact(next="aging"))
    cls.benign_age_check = benign_age_check

    @Rule(Answer(ident="aging", text=MATCH.response), Fact(condition_group="benign_likely"))
    def benign_location(self, response):
        self.declare(Fact(next="benign_locations"))
    cls.benign_location = benign_location

    # Nails/Serious Sub-branch
    @Rule(Answer(ident="thickened_nails", text="yes"), Fact(sub_branch="nails_serious"))
    def nail_path(self):
        self.declare(Fact(next="discoloration"))
        self.declare(Fact(condition_group="nail_likely"))
    cls.nail_path = nail_path

    @Rule(Answer(ident="thickened_nails", text="no"), Fact(sub_branch="nails_serious"))
    def serious_path(self):
        self.declare(Fact(next="ulcer"))
        self.declare(Fact(condition_group="serious_likely"))
    cls.serious_path = serious_path

    # Nail disorder path
    @Rule(Answer(ident="discoloration", text=MATCH.response), Fact(condition_group="nail_likely"))
    def nail_triggers(self, response):
        self.declare(Fact(next="moisture_exposure"))
    cls.nail_triggers = nail_triggers

    @Rule(Answer(ident="moisture_exposure", text=MATCH.response), Fact(condition_group="nail_likely"))
    def nail_location(self, response):
        self.declare(Fact(next="nail_locations"))
    cls.nail_location = nail_location

    # Serious conditions path
    @Rule(Answer(ident="ulcer", text="yes"), Fact(condition_group="serious_likely"))
    def malignant_path(self):
        self.declare(Fact(next="pain"))
    cls.malignant_path = malignant_path

    @Rule(Answer(ident="ulcer", text="no"), Fact(condition_group="serious_likely"))
    def systemic_path(self):
        self.declare(Fact(next="joint_pain"))
    cls.systemic_path = systemic_path

    @Rule(Answer(ident="pain", text=MATCH.response), Fact(condition_group="serious_likely"))
    def malignant_location(self, response):
        self.declare(Fact(next="malignant_locations"))
    cls.malignant_location = malignant_location

    @Rule(Answer(ident="joint_pain", text=MATCH.response), Fact(condition_group="serious_likely"))
    def systemic_location(self, response):
        # Using malignant_locations for systemic too
        self.declare(Fact(next="malignant_locations"))
    cls.systemic_location = systemic_location

    # CELLULITIS BRANCH
    @Rule(Answer(ident="redness", text="yes"))
    def cellulitis_branch(self):
        self.declare(Fact(next="pain"))
        self.declare(Fact(condition_group="cellulitis_likely"))

    cls.cellulitis_branch = cellulitis_branch

    @Rule(
        Answer(ident="pain", text=MATCH.response),
        Fact(condition_group="cellulitis_likely"),
    )
    def cellulitis_progress(self, response):
        self.declare(Fact(next="swelling"))

    cls.cellulitis_progress = cellulitis_progress

    @Rule(
        Answer(ident="swelling", text=MATCH.response),
        Fact(condition_group="cellulitis_likely"),
    )
    def cellulitis_location(self, response):
        self.declare(Fact(next="cellulitis_locations"))

    cls.cellulitis_location = cellulitis_location

    # IMPETIGO BRANCH
    @Rule(Answer(ident="blisters", text="yes"))
    def impetigo_branch(self):
        self.declare(Fact(next="crusting"))
        self.declare(Fact(condition_group="impetigo_likely"))

    cls.impetigo_branch = impetigo_branch

    @Rule(
        Answer(ident="crusting", text=MATCH.response),
        Fact(condition_group="impetigo_likely"),
    )
    def impetigo_location(self, response):
        self.declare(Fact(next="impetigo_locations"))

    cls.impetigo_location = impetigo_location

    # LUPUS BRANCH
    @Rule(Answer(ident="rash", text="yes"))
    def lupus_branch(self):
        self.declare(Fact(next="joint_pain"))
        self.declare(Fact(condition_group="lupus_likely"))

    cls.lupus_branch = lupus_branch

    @Rule(
        Answer(ident="joint_pain", text=MATCH.response),
        Fact(condition_group="lupus_likely"),
    )
    def lupus_progress(self, response):
        self.declare(Fact(next="photosensitivity"))

    cls.lupus_progress = lupus_progress

    @Rule(
        Answer(ident="photosensitivity", text=MATCH.response),
        Fact(condition_group="lupus_likely"),
    )
    def lupus_location(self, response):
        self.declare(Fact(next="lupus_locations"))

    cls.lupus_location = lupus_location

    # CONNECTIVE TISSUE DISEASES BRANCH
    @Rule(Answer(ident="joint_pain", text="yes"))
    def connective_branch(self):
        self.declare(Fact(next="rash"))
        self.declare(Fact(condition_group="connective_likely"))

    cls.connective_branch = connective_branch

    @Rule(
        Answer(ident="rash", text=MATCH.response),
        Fact(condition_group="connective_likely"),
    )
    def connective_location(self, response):
        self.declare(Fact(next="connective_tissue_locations"))

    cls.connective_location = connective_location

    # MELANOMA BRANCH
    @Rule(Answer(ident="discoloration", text="yes"))
    def melanoma_branch(self):
        self.declare(Fact(next="mole_change"))
        self.declare(Fact(condition_group="melanoma_likely"))

    cls.melanoma_branch = melanoma_branch

    @Rule(
        Answer(ident="mole_change", text=MATCH.response),
        Fact(condition_group="melanoma_likely"),
    )
    def melanoma_location(self, response):
        self.declare(Fact(next="melanoma_locations"))

    cls.melanoma_location = melanoma_location

    # NEVI AND MOLES BRANCH
    @Rule(Answer(ident="mole_change", text="yes"))
    def nevi_branch(self):
        self.declare(Fact(next="itching"))
        self.declare(Fact(condition_group="nevi_likely"))

    cls.nevi_branch = nevi_branch

    @Rule(
        Answer(ident="itching", text=MATCH.response),
        Fact(condition_group="nevi_likely"),
    )
    def nevi_location(self, response):
        self.declare(Fact(next="nevi_locations"))

    cls.nevi_location = nevi_location

    # SCABIES BRANCH
    @Rule(Answer(ident="itching", text="yes"))
    def scabies_branch(self):
        self.declare(Fact(next="rash_between_fingers"))
        self.declare(Fact(condition_group="scabies_likely"))

    cls.scabies_branch = scabies_branch

    @Rule(
        Answer(ident="rash_between_fingers", text=MATCH.response),
        Fact(condition_group="scabies_likely"),
    )
    def scabies_location(self, response):
        self.declare(Fact(next="scabies_locations"))

    cls.scabies_location = scabies_location

    # LYME DISEASE BRANCH
    @Rule(Answer(ident="rash", text="yes"))
    def lyme_branch(self):
        self.declare(Fact(next="joint_pain"))
        self.declare(Fact(condition_group="lyme_likely"))

    cls.lyme_branch = lyme_branch

    @Rule(
        Answer(ident="joint_pain", text=MATCH.response),
        Fact(condition_group="lyme_likely"),
    )
    def lyme_progress(self, response):
        self.declare(Fact(next="tick_bite"))

    cls.lyme_progress = lyme_progress

    @Rule(
        Answer(ident="tick_bite", text=MATCH.response),
        Fact(condition_group="lyme_likely"),
    )
    def lyme_location(self, response):
        self.declare(Fact(next="lyme_disease_locations"))

    cls.lyme_location = lyme_location

    # TERMINAL RULES - End diagnosis flow
    terminal_locations = [
        "psoriasis_locations",
        "eczema_locations",
        "fungal_locations",
        "contact_locations",
        "viral_locations",
        "benign_locations",
        "nail_locations",
        "malignant_locations",
        "cellulitis_locations",
        "impetigo_locations",
        "lupus_locations",
        "connective_tissue_locations",
        "melanoma_locations",
        "nevi_locations",
        "scabies_locations",
        "lyme_disease_locations",
    ]

    for location in terminal_locations:
        def make_terminal_rule(loc):
            def terminal_rule(self, response):
                self.declare(Fact(next=None))
                self.declare(Fact(diagnosis_ready=True))
            terminal_rule.__name__ = f"end_at_{loc}"
            return Rule(Answer(ident=loc, text=MATCH.response))(terminal_rule)

        setattr(cls, f"end_at_{location}", make_terminal_rule(location))

    return cls
