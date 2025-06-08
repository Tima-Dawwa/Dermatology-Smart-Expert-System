from ExpertSystem.facts import *
from ExpertSystem.Data.disease import diseases
from ExpertSystem.Questions.question import basic_questions
from ExpertSystem.Questions.question_flow import apply_question_flow
from experta import *


class DermatologyExpert(KnowledgeEngine):

    def __init__(self):
        super().__init__()
        self.patient_age = None
        self.condition_duration = None  # Add duration tracking

    @DefFacts()
    def initial_questions(self):
        for d in diseases:
            yield d
        for q in basic_questions:
            yield q

    @Rule(
        Fact(next=MATCH.next_q),
        question(ident=MATCH.next_q, text=MATCH.text,
                 valid=MATCH.valid, Type=MATCH.Type),
        NOT(Answer(ident=MATCH.next_q)),
    )
    def ask_next_question(self, next_q, text, valid, Type):
        for fact in self.facts.values():
            if isinstance(fact, Diagnosis):
                return
        response = self.ask_user(text, Type, valid)
        cf = 1.0 if response == "yes" else 0.0
        self.declare(Answer(ident=next_q, text=response, cf=cf))

        # Capture age for later use
        if next_q == "age_range":
            self.patient_age = self.parse_age_range(response)

        # Capture duration for later use
        elif next_q == "common_duration":
            self.condition_duration = self.parse_duration(response)

    def parse_age_range(self, age_response):
        """Parse age range response and return midpoint for calculations"""
        age_mappings = {
            "child (0-12)": 6,
            "teenager (13-19)": 16,
            "young adult (20-35)": 27,
            "middle-aged (36-55)": 45,
            "senior (56+)": 65
        }
        # Default to 30 if unknown
        return age_mappings.get(age_response.lower(), 30)

    def parse_duration(self, duration_response):
        """Parse duration response and return value in days for calculations"""
        duration_mappings = {
            "less than 1 week": 3,
            "1-2 weeks": 10,
            "2-4 weeks": 21,
            "1-3 months": 60,
            "3-6 months": 135,
            "6 months - 1 year": 270,
            "more than 1 year": 500
        }
        # Default to 30 days if unknown
        return duration_mappings.get(duration_response.lower(), 30)

    def ask_user(self, question_text, Type, valid=None):
        print("\n🧐 " + question_text)
        if Type == "multi" and valid:
            print(f"Valid responses: {', '.join(valid)}")
        response = input("Your answer: ").strip().lower()
        return response

    @Rule(Fact(next=None))
    def diagnosis_complete(self):
        self.declare(Fact(diagnosis_complete=True))

    def combine_cf(self, cf1, cf2):
        if cf1 >= 0 and cf2 >= 0:
            return cf1 + cf2 * (1 - cf1)
        elif cf1 < 0 and cf2 < 0:
            return cf1 + cf2 * (1 + cf1)
        else:
            return (cf1 + cf2) / (1 - min(abs(cf1), abs(cf2)))

    def calculate_age_factor(self, disease_name):
        """Calculate age-based confidence factor for a disease"""
        if self.patient_age is None:
            return 1.0  # No age adjustment if age unknown

        # Find the disease info
        disease_info = None
        for fact in self.facts.values():
            if isinstance(fact, DiseaseInfo) and fact["name"] == disease_name:
                disease_info = fact
                break

        if not disease_info:
            return 1.0

        age_min = disease_info.get("age_min", 0)
        age_max = disease_info.get("age_max", 100)

        # If patient age is within typical range, no penalty
        if age_min <= self.patient_age <= age_max:
            return 1.0

        # Calculate penalty based on how far outside the range
        if self.patient_age < age_min:
            distance = age_min - self.patient_age
        else:
            distance = self.patient_age - age_max

        # Apply exponential decay penalty - more distance = lower confidence
        # Maximum penalty is 50% (factor of 0.5)
        penalty_factor = max(0.5, 1.0 - (distance / 50.0))
        return penalty_factor

    def calculate_duration_factor(self, disease_name):
        """Calculate duration-based confidence factor for a disease"""
        if self.condition_duration is None:
            return 1.0  # No duration adjustment if duration unknown

        # Find the disease info
        disease_info = None
        for fact in self.facts.values():
            if isinstance(fact, DiseaseInfo) and fact["name"] == disease_name:
                disease_info = fact
                break

        if not disease_info:
            return 1.0

        # Get typical duration range for the disease (in days)
        duration_min = disease_info.get("duration_min", 1)
        duration_max = disease_info.get("duration_max", 365)

        # If condition duration is within typical range, no penalty
        if duration_min <= self.condition_duration <= duration_max:
            return 1.0

        # Calculate penalty based on how far outside the range
        if self.condition_duration < duration_min:
            # Condition too short for this disease
            distance = duration_min - self.condition_duration
            penalty_factor = max(0.6, 1.0 - (distance / duration_min * 0.4))
        else:
            # Condition too long for this disease
            distance = self.condition_duration - duration_max
            penalty_factor = max(0.7, 1.0 - (distance / duration_max * 0.3))

        return penalty_factor

    def get_duration_category(self):
        """Get duration category string for display"""
        if self.condition_duration is None:
            return "Unknown"
        elif self.condition_duration <= 7:
            return "Less than 1 week"
        elif self.condition_duration <= 14:
            return "1-2 weeks"
        elif self.condition_duration <= 30:
            return "2-4 weeks"
        elif self.condition_duration <= 90:
            return "1-3 months"
        elif self.condition_duration <= 180:
            return "3-6 months"
        elif self.condition_duration <= 365:
            return "6 months - 1 year"
        else:
            return "More than 1 year"

    def declare_or_update_diagnosis(self, disease, reasoning, new_cf):
        # Apply age-based adjustment
        age_factor = self.calculate_age_factor(disease)

        # Apply duration-based adjustment
        duration_factor = self.calculate_duration_factor(disease)

        # Combine both adjustments
        adjusted_cf = new_cf * age_factor * duration_factor

        # Add adjustment notes if adjustments were made
        adjustment_notes = []
        if age_factor < 1.0:
            adjustment_notes.append(f"Age-adjusted: {age_factor:.2f}")
        if duration_factor < 1.0:
            adjustment_notes.append(
                f"Duration-adjusted: {duration_factor:.2f}")

        if adjustment_notes:
            adjustment_note = f" ({', '.join(adjustment_notes)})"
            reasoning += adjustment_note

        for fact in self.facts.values():
            if isinstance(fact, Diagnosis) and fact["disease"] == disease:
                combined_cf = self.combine_cf(fact["cf"], adjusted_cf)
                self.modify(fact, cf=combined_cf, reasoning=reasoning +
                            f" (updated CF: {combined_cf:.2f})")
                return
        self.declare(Diagnosis(disease=disease,
                     reasoning=reasoning, cf=adjusted_cf))

    # ECZEMA/ATOPIC DERMATITIS RULES
    @Rule(Answer(ident="itching", text="yes", cf=MATCH.cf1),
          Answer(ident="dryness", text="yes", cf=MATCH.cf2),
          Answer(ident="redness_and_inflammation", text="yes", cf=MATCH.cf3))
    def diagnose_eczema_comprehensive(self, cf1, cf2, cf3):
        cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
        self.declare_or_update_diagnosis(
            disease="Eczema",
            reasoning="Itching, dryness, and inflammation are key symptoms of eczema.",
            new_cf=cf * 0.9
        )

    @Rule(Answer(ident="itching", text="yes", cf=MATCH.cf1),
          Answer(ident="dry_skin", text="yes", cf=MATCH.cf2))
    def diagnose_atopic_dermatitis(self, cf1, cf2):
        cf = self.combine_cf(cf1, cf2)
        self.declare_or_update_diagnosis(
            disease="Atopic Dermatitis",
            reasoning="Itching and dry skin are primary symptoms of atopic dermatitis.",
            new_cf=cf * 0.85
        )

    # PSORIASIS RULES
    @Rule(Answer(ident="scaling", text="yes", cf=MATCH.cf1),
          Answer(ident="redness", text="yes", cf=MATCH.cf2),
          Answer(ident="stress", text="yes", cf=MATCH.cf3))
    def diagnose_psoriasis_comprehensive(self, cf1, cf2, cf3):
        cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
        self.declare_or_update_diagnosis(
            disease="Psoriasis",
            reasoning="Scaling, redness, and stress trigger match psoriasis profile.",
            new_cf=cf * 0.9
        )

    @Rule(Answer(ident="scaling", text="yes", cf=MATCH.cf1),
          Answer(ident="redness", text="yes", cf=MATCH.cf2))
    def diagnose_psoriasis_simple(self, cf1, cf2):
        cf = self.combine_cf(cf1, cf2)
        self.declare_or_update_diagnosis(
            disease="Psoriasis",
            reasoning="Scaling and redness are characteristic of psoriasis.",
            new_cf=cf * 0.75
        )

    # FUNGAL INFECTIONS RULES
    @Rule(Answer(ident="ring_shaped_rash", text="yes", cf=MATCH.cf1),
          Answer(ident="scaly_skin", text="yes", cf=MATCH.cf2),
          Answer(ident="warm_moist_environments", text="yes", cf=MATCH.cf3))
    def diagnose_tinea_ringworm(self, cf1, cf2, cf3):
        cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
        self.declare_or_update_diagnosis(
            disease="Tinea (Ringworm)",
            reasoning="Ring-shaped rash, scaling, and warm moist environment exposure indicate ringworm.",
            new_cf=cf * 0.9
        )

    @Rule(Answer(ident="red_rash", text="yes", cf=MATCH.cf1),
          Answer(ident="white_patches_oral_vaginal", text="yes", cf=MATCH.cf2),
          Answer(ident="itching_or_burning", text="yes", cf=MATCH.cf3))
    def diagnose_candidiasis(self, cf1, cf2, cf3):
        cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
        self.declare_or_update_diagnosis(
            disease="Candidiasis",
            reasoning="Red rash, white patches, and burning suggest candidiasis.",
            new_cf=cf * 0.9
        )

    @Rule(Answer(ident="discolored_patches", text="yes", cf=MATCH.cf1),
          Answer(ident="mild_scaling", text="yes", cf=MATCH.cf2),
          Answer(ident="humidity", text="yes", cf=MATCH.cf3))
    def diagnose_tinea_versicolor(self, cf1, cf2, cf3):
        cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
        self.declare_or_update_diagnosis(
            disease="Tinea Versicolor",
            reasoning="Discolored patches with mild scaling in humid conditions suggest tinea versicolor.",
            new_cf=cf * 0.85
        )

    @Rule(Answer(ident="thickened_nails", text="yes", cf=MATCH.cf1),
          Answer(ident="discoloration", text="yes", cf=MATCH.cf2),
          Answer(ident="brittle_or_crumbly_nails", text="yes", cf=MATCH.cf3))
    def diagnose_onychomycosis(self, cf1, cf2, cf3):
        cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
        self.declare_or_update_diagnosis(
            disease="Onychomycosis",
            reasoning="Thickened, discolored, brittle nails indicate nail fungal infection.",
            new_cf=cf * 0.9
        )

    # BENIGN GROWTHS RULES
    @Rule(Answer(ident="waxy_appearance", text="yes", cf=MATCH.cf1),
          Answer(ident="color_change_brown_black", text="yes", cf=MATCH.cf2),
          Answer(ident="aging", text="yes", cf=MATCH.cf3))
    def diagnose_seborrheic_keratoses(self, cf1, cf2, cf3):
        cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
        self.declare_or_update_diagnosis(
            disease="Seborrheic Keratoses",
            reasoning="Waxy appearance, brown/black color change with aging suggest seborrheic keratoses.",
            new_cf=cf * 0.9
        )

    @Rule(Answer(ident="soft_lump_under_skin", text="yes", cf=MATCH.cf1),
          Answer(ident="slow_growth", text="yes", cf=MATCH.cf2),
          Answer(ident="non_painful", text="yes", cf=MATCH.cf3))
    def diagnose_lipoma(self, cf1, cf2, cf3):
        cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
        self.declare_or_update_diagnosis(
            disease="Lipoma",
            reasoning="Soft, slowly growing, painless lump indicates lipoma.",
            new_cf=cf * 0.85
        )

    @Rule(Answer(ident="firm_nodule", text="yes", cf=MATCH.cf1),
          Answer(ident="pigmentation", text="yes", cf=MATCH.cf2),
          Answer(ident="dimpling_when_pinched", text="yes", cf=MATCH.cf3))
    def diagnose_dermatofibroma(self, cf1, cf2, cf3):
        cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
        self.declare_or_update_diagnosis(
            disease="Dermatofibroma",
            reasoning="Firm nodule with pigmentation and dimpling when pinched indicates dermatofibroma.",
            new_cf=cf * 0.9
        )

    @Rule(Answer(ident="rough_raised_bumps", text="yes", cf=MATCH.cf1),
          Answer(ident="flesh_colored_or_darker", text="yes", cf=MATCH.cf2),
          Answer(ident="hpv_infection", text="yes", cf=MATCH.cf3))
    def diagnose_warts(self, cf1, cf2, cf3):
        cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
        self.declare_or_update_diagnosis(
            disease="Warts (Verruca Vulgaris)",
            reasoning="Rough raised bumps, flesh-colored appearance, and HPV history indicate warts.",
            new_cf=cf * 0.9
        )

    @Rule(Answer(ident="pearly_dome_shaped_bumps", text="yes", cf=MATCH.cf1),
          Answer(ident="central_dimple", text="yes", cf=MATCH.cf2),
          Answer(ident="skin_to_skin_contact", text="yes", cf=MATCH.cf3))
    def diagnose_molluscum_contagiosum(self, cf1, cf2, cf3):
        cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
        self.declare_or_update_diagnosis(
            disease="Molluscum Contagiosum",
            reasoning="Pearly dome-shaped bumps with central dimple and contact history indicate molluscum contagiosum.",
            new_cf=cf * 0.9
        )

    # VIRAL INFECTIONS RULES
    @Rule(Answer(ident="painful_blisters", text="yes", cf=MATCH.cf1),
          Answer(ident="tingling_or_burning_before_rash",
                 text="yes", cf=MATCH.cf2),
          Answer(ident="stress", text="yes", cf=MATCH.cf3))
    def diagnose_hsv(self, cf1, cf2, cf3):
        cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
        self.declare_or_update_diagnosis(
            disease="Herpes Simplex Virus (HSV)",
            reasoning="Painful blisters with tingling/burning and stress trigger indicate HSV.",
            new_cf=cf * 0.9
        )

    @Rule(Answer(ident="painful_rash", text="yes", cf=MATCH.cf1),
          Answer(ident="blistering", text="yes", cf=MATCH.cf2),
          Answer(ident="previous_chickenpox_infection", text="yes", cf=MATCH.cf3))
    def diagnose_herpes_zoster(self, cf1, cf2, cf3):
        cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
        self.declare_or_update_diagnosis(
            disease="Herpes Zoster (Shingles)",
            reasoning="Painful blistering rash with previous chickenpox history indicates shingles.",
            new_cf=cf * 0.9
        )

    # NAIL DISORDERS RULES
    @Rule(Answer(ident="swelling_around_nail", text="yes", cf=MATCH.cf1),
          Answer(ident="redness_and_tenderness", text="yes", cf=MATCH.cf2),
          Answer(ident="nail_biting", text="yes", cf=MATCH.cf3))
    def diagnose_paronychia(self, cf1, cf2, cf3):
        cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
        self.declare_or_update_diagnosis(
            disease="Paronychia",
            reasoning="Nail swelling, redness, tenderness with nail biting history indicate paronychia.",
            new_cf=cf * 0.9
        )

    @Rule(Answer(ident="pitting", text="yes", cf=MATCH.cf1),
          Answer(ident="nail_separation", text="yes", cf=MATCH.cf2),
          Answer(ident="psoriasis_flare_ups", text="yes", cf=MATCH.cf3))
    def diagnose_nail_psoriasis(self, cf1, cf2, cf3):
        cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
        self.declare_or_update_diagnosis(
            disease="Nail Psoriasis",
            reasoning="Nail pitting, separation with psoriasis flare-ups indicate nail psoriasis.",
            new_cf=cf * 0.9
        )

    @Rule(Answer(ident="horizontal_nail_grooves", text="yes", cf=MATCH.cf1),
          Answer(ident="severe_illness", text="yes", cf=MATCH.cf2))
    def diagnose_beaus_lines(self, cf1, cf2):
        cf = self.combine_cf(cf1, cf2)
        self.declare_or_update_diagnosis(
            disease="Beau's Lines",
            reasoning="Horizontal nail grooves after severe illness indicate Beau's lines.",
            new_cf=cf * 0.85
        )

    @Rule(Answer(ident="concave_nail_shape", text="yes", cf=MATCH.cf1),
          Answer(ident="thin_brittle_nails", text="yes", cf=MATCH.cf2),
          Answer(ident="iron_deficiency", text="yes", cf=MATCH.cf3))
    def diagnose_koilonychia(self, cf1, cf2, cf3):
        cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
        self.declare_or_update_diagnosis(
            disease="Koilonychia (Spoon Nails)",
            reasoning="Concave nail shape, brittle nails with iron deficiency indicate koilonychia.",
            new_cf=cf * 0.9
        )

    # ACNE/ROSACEA RULES
    @Rule(Answer(ident="pimples", text="yes", cf=MATCH.cf1),
          Answer(ident="oiliness", text="yes", cf=MATCH.cf2),
          Answer(ident="hormones", text="yes", cf=MATCH.cf3))
    def diagnose_acne_rosacea(self, cf1, cf2, cf3):
        cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
        self.declare_or_update_diagnosis(
            disease="Acne and Rosacea",
            reasoning="Pimples, oiliness, and hormonal changes indicate acne/rosacea.",
            new_cf=cf * 0.85
        )

    # HAIR LOSS RULES
    @Rule(Answer(ident="hair_thinning", text="yes", cf=MATCH.cf1),
          Answer(ident="patchy_baldness", text="yes", cf=MATCH.cf2),
          Answer(ident="autoimmune_disorders", text="yes", cf=MATCH.cf3))
    def diagnose_hair_loss(self, cf1, cf2, cf3):
        cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
        self.declare_or_update_diagnosis(
            disease="Hair Loss, Alopecia, and other Hair Diseases",
            reasoning="Hair thinning, patchy baldness with autoimmune history indicate alopecia.",
            new_cf=cf * 0.9
        )

    # CONTACT DERMATITIS RULES
    @Rule(Answer(ident="rash", text="yes", cf=MATCH.cf1),
          Answer(ident="blisters", text="yes", cf=MATCH.cf2),
          Answer(ident="plants", text="yes", cf=MATCH.cf3))
    def diagnose_contact_dermatitis(self, cf1, cf2, cf3):
        cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
        self.declare_or_update_diagnosis(
            disease="Poison Ivy and other Contact Dermatitis",
            reasoning="Rash with blisters after plant exposure indicates contact dermatitis.",
            new_cf=cf * 0.9
        )

    # EXANTHEMS AND DRUG ERUPTIONS RULES
    @Rule(Answer(ident="rash", text="yes", cf=MATCH.cf1),
          Answer(ident="viral_infections_trigger", text="yes", cf=MATCH.cf2))
    def diagnose_exanthems(self, cf1, cf2):
        cf = self.combine_cf(cf1, cf2)
        self.declare_or_update_diagnosis(
            disease="Exanthems and Drug Eruptions",
            reasoning="Rash following viral infection suggests exanthem.",
            new_cf=cf * 0.8
        )

    @Rule(Answer(ident="rash", text="yes", cf=MATCH.cf1),
          Answer(ident="medications_trigger", text="yes", cf=MATCH.cf2))
    def diagnose_drug_eruptions(self, cf1, cf2):
        cf = self.combine_cf(cf1, cf2)
        self.declare_or_update_diagnosis(
            disease="Exanthems and Drug Eruptions",
            reasoning="Rash after starting new medications suggests drug eruption.",
            new_cf=cf * 0.85
        )

    # PIGMENTATION DISORDERS RULES
    @Rule(Answer(ident="white_or_dark_patches", text="yes", cf=MATCH.cf1),
          Answer(ident="irregular_pigmentation", text="yes", cf=MATCH.cf2),
          Answer(ident="sun_exposure", text="yes", cf=MATCH.cf3))
    def diagnose_pigmentation_disorders(self, cf1, cf2, cf3):
        cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
        self.declare_or_update_diagnosis(
            disease="Light Diseases and Disorders of Pigmentation",
            reasoning="White/dark patches with irregular pigmentation and sun exposure suggest pigmentation disorder.",
            new_cf=cf * 0.85
        )

    # SERIOUS/MALIGNANT CONDITIONS RULES
    @Rule(Answer(ident="pain", text="yes", cf=MATCH.cf1),
          Answer(ident="ulcer", text="yes", cf=MATCH.cf2),
          Answer(ident="uv_radiation", text="yes", cf=MATCH.cf3))
    def diagnose_malignant_lesions(self, cf1, cf2, cf3):
        cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
        self.declare_or_update_diagnosis(
            disease="Malignant Skin Lesions",
            reasoning="Painful ulcers with UV exposure history suggest malignant skin lesions.",
            new_cf=cf * 0.9
        )

    @Rule(Answer(ident="joint_pain", text="yes", cf=MATCH.cf1),
          Answer(ident="autoimmune_response", text="yes", cf=MATCH.cf2))
    def diagnose_systemic_disease(self, cf1, cf2):
        cf = self.combine_cf(cf1, cf2)
        self.declare_or_update_diagnosis(
            disease="Systemic Disease",
            reasoning="Joint pain with autoimmune response suggests systemic disease with skin manifestations.",
            new_cf=cf * 0.85
        )

    @Rule(Answer(ident="ulcer", text="yes", cf=MATCH.cf1),
          Answer(ident="pain", text="yes", cf=MATCH.cf2),
          Answer(ident="infections", text="yes", cf=MATCH.cf3))
    def diagnose_vasculitis(self, cf1, cf2, cf3):
        cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
        self.declare_or_update_diagnosis(
            disease="Vasculitis",
            reasoning="Painful ulcers with infection history suggest vasculitis.",
            new_cf=cf * 0.85
        )

    @Rule(Answer(ident="blisters", text="yes", cf=MATCH.cf1),
          Answer(ident="pain", text="yes", cf=MATCH.cf2),
          Answer(ident="autoimmune_response", text="yes", cf=MATCH.cf3))
    def diagnose_bullous_disease(self, cf1, cf2, cf3):
        cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
        self.declare_or_update_diagnosis(
            disease="Bullous Disease",
            reasoning="Painful blisters with autoimmune response suggest bullous disease.",
            new_cf=cf * 0.9
        )

    @Rule(Answer(ident="blisters", text="yes", cf=MATCH.cf1),
          Answer(ident="pain", text="yes", cf=MATCH.cf2),
          Answer(ident="sexual_contact", text="yes", cf=MATCH.cf3))
    def diagnose_herpes_stds(self, cf1, cf2, cf3):
        cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
        self.declare_or_update_diagnosis(
            disease="Herpes / STDs",
            reasoning="Painful blisters with sexual contact history suggest herpes or STDs.",
            new_cf=cf * 0.9
        )

@Rule(
    Answer(ident="red_swollen_skin", text="yes", cf=MATCH.cf1),
    Answer(ident="warmth", text="yes", cf=MATCH.cf2),
    Answer(ident="pain", text="yes", cf=MATCH.cf3),
)
def diagnose_cellulitis(self, cf1, cf2, cf3):
    cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
    self.declare_or_update_diagnosis(
        disease="Cellulitis",
        reasoning="Red, swollen, warm, and painful skin suggests cellulitis.",
        new_cf=cf * 0.9,
    )

@Rule(
    Answer(ident="honey_crusted_lesions", text="yes", cf=MATCH.cf1),
    Answer(ident="face_and_extremities", text="yes", cf=MATCH.cf2),
)
def diagnose_impetigo(self, cf1, cf2):
    cf = self.combine_cf(cf1, cf2)
    self.declare_or_update_diagnosis(
        disease="Impetigo",
        reasoning="Honey-crusted lesions on face and extremities are characteristic of impetigo.",
        new_cf=cf * 0.85,
    )

@Rule(
    Answer(ident="butterfly_rash", text="yes", cf=MATCH.cf1),
    Answer(ident="joint_pain", text="yes", cf=MATCH.cf2),
    Answer(ident="fatigue", text="yes", cf=MATCH.cf3),
)
def diagnose_lupus(self, cf1, cf2, cf3):
    cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
    self.declare_or_update_diagnosis(
        disease="Lupus",
        reasoning="Butterfly rash, joint pain, and fatigue suggest systemic lupus erythematosus.",
        new_cf=cf * 0.9,
    )

@Rule(
    Answer(ident="joint_stiffness", text="yes", cf=MATCH.cf1),
    Answer(ident="raynaud_phenomenon", text="yes", cf=MATCH.cf2),
    Answer(ident="skin_thickening", text="yes", cf=MATCH.cf3),
)
def diagnose_connective_tissue_disease(self, cf1, cf2, cf3):
    cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
    self.declare_or_update_diagnosis(
        disease="Connective Tissue Disease",
        reasoning="Joint stiffness, Raynaud’s phenomenon, and skin thickening suggest connective tissue disease.",
        new_cf=cf * 0.9,
    )

@Rule(
    Answer(ident="asymmetry", text="yes", cf=MATCH.cf1),
    Answer(ident="irregular_border", text="yes", cf=MATCH.cf2),
    Answer(ident="color_variegation", text="yes", cf=MATCH.cf3),
)
def diagnose_melanoma(self, cf1, cf2, cf3):
    cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
    self.declare_or_update_diagnosis(
        disease="Melanoma Skin Cancer",
        reasoning="Asymmetry, irregular borders, and color variegation are hallmarks of melanoma.",
        new_cf=cf * 0.95,
    )

@Rule(
    Answer(ident="symmetrical_mole", text="yes", cf=MATCH.cf1),
    Answer(ident="uniform_color", text="yes", cf=MATCH.cf2),
    Answer(ident="stable_size", text="yes", cf=MATCH.cf3),
)
def diagnose_nevi_moles(self, cf1, cf2, cf3):
    cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
    self.declare_or_update_diagnosis(
        disease="Nevi and Moles",
        reasoning="Symmetrical shape, uniform color, and stable size are features of benign nevi.",
        new_cf=cf * 0.9,
    )

@Rule(
    Answer(ident="intense_night_itching", text="yes", cf=MATCH.cf1),
    Answer(ident="burrow_tracks", text="yes", cf=MATCH.cf2),
    Answer(ident="close_contact_history", text="yes", cf=MATCH.cf3),
)
def diagnose_scabies(self, cf1, cf2, cf3):
    cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
    self.declare_or_update_diagnosis(
        disease="Scabies",
        reasoning="Intense itching at night, burrows, and close contact history suggest scabies.",
        new_cf=cf * 0.9,
    )

@Rule(
    Answer(ident="bullseye_rash", text="yes", cf=MATCH.cf1),
    Answer(ident="tick_bite", text="yes", cf=MATCH.cf2),
    Answer(ident="joint_pain", text="yes", cf=MATCH.cf3),
)
def diagnose_lyme_disease(self, cf1, cf2, cf3):
    cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
    self.declare_or_update_diagnosis(
        disease="Lyme Disease",
        reasoning="Bullseye rash, tick bite, and joint pain indicate Lyme disease.",
        new_cf=cf * 0.9,
    )

    # TRIGGER FINAL DIAGNOSIS
    @Rule(Fact(diagnosis_ready=True), salience=-10)
    def trigger_final_diagnosis(self):
        self.get_final_diagnosis()

    def get_final_diagnosis(self):
        diagnoses = []
        for fact in self.facts.values():
            if isinstance(fact, Diagnosis):
                diagnoses.append(fact)

        if diagnoses:
            # Sort by confidence
            diagnoses.sort(key=lambda x: x["cf"], reverse=True)

            print("\n" + "="*50)
            print("🏥 DIAGNOSTIC RESULTS")
            print("="*50)

            if self.patient_age:
                print(f"Patient Age Category: {self.get_age_category()}")
            if self.condition_duration:
                print(f"Condition Duration: {self.get_duration_category()}")
            print("-" * 50)

            for i, diagnosis in enumerate(diagnoses[:3], 1):  # Show top 3
                print(f"\n{i}. {diagnosis['disease']}")
                print(f"   Confidence: {diagnosis['cf'] * 100:.1f}%")
                print(f"   Reasoning: {diagnosis['reasoning']}")

                # Find disease info for additional details
                for disease_fact in self.facts.values():
                    if isinstance(disease_fact, DiseaseInfo) and disease_fact["name"] == diagnosis['disease']:
                        print(
                            f"   Description: {disease_fact.get('description', 'No description available')}")
                        if disease_fact.get('age_min') and disease_fact.get('age_max'):
                            print(
                                f"   Typical Age Range: {disease_fact['age_min']}-{disease_fact['age_max']} years")
                        if disease_fact.get('duration_min') and disease_fact.get('duration_max'):
                            print(
                                f"   Typical Duration: {disease_fact['duration_min']}-{disease_fact['duration_max']} days")
                        break

            print("\n" + "="*50)
            print("⚠️  DISCLAIMER: This is a preliminary assessment.")
            print("Age-based adjustments have been applied to improve accuracy.")
            print(
                "Please consult a healthcare professional for proper diagnosis and treatment.")
            print("="*50)
        else:
            print(
                "\n⚠️ No confident diagnosis could be made based on the provided symptoms.")
            print(
                "Consider providing more detailed information or consulting a healthcare professional.")

    def get_age_category(self):
        """Get age category string for display"""
        if self.patient_age <= 12:
            return "Child (0-12)"
        elif self.patient_age <= 19:
            return "Teenager (13-19)"
        elif self.patient_age <= 35:
            return "Young Adult (20-35)"
        elif self.patient_age <= 55:
            return "Middle-aged (36-55)"
        else:
            return "Senior (56+)"


# Apply the question flow decorator
apply_question_flow(DermatologyExpert)
