from ExpertSystem.facts import *
from ExpertSystem.Data.disease import diseases
from ExpertSystem.Questions.question import basic_questions
from ExpertSystem.Questions.question_flow import apply_question_flow
from experta import *


class DermatologyExpert(KnowledgeEngine):

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

    def declare_or_update_diagnosis(self, disease, reasoning, new_cf):
        for fact in self.facts.values():
            if isinstance(fact, Diagnosis) and fact["disease"] == disease:
                combined_cf = self.combine_cf(fact["cf"], new_cf)
                self.modify(fact, cf=combined_cf, reasoning=reasoning +
                            f" (updated CF: {combined_cf:.2f})")
                return
        self.declare(Diagnosis(disease=disease,
                     reasoning=reasoning, cf=new_cf))

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

            for i, diagnosis in enumerate(diagnoses[:3], 1):  # Show top 3
                print(f"\n{i}. {diagnosis['disease']}")
                print(f"   Confidence: {diagnosis['cf'] * 100:.1f}%")
                print(f"   Reasoning: {diagnosis['reasoning']}")

                # Find disease info for additional details
                for disease_fact in self.facts.values():
                    if (isinstance(disease_fact, DiseaseInfo) and
                            disease_fact["name"] == diagnosis['disease']):
                        if "common_treatments" in disease_fact:
                            print(
                                f"   Common Treatments: {', '.join(disease_fact['common_treatments'])}")
                        if "notes" in disease_fact:
                            print(f"   Notes: {disease_fact['notes']}")
                        break

            print("\n" + "="*50)
            print("⚠️  DISCLAIMER: This is a preliminary assessment.")
            print(
                "Please consult a healthcare professional for proper diagnosis and treatment.")
            print("="*50)
        else:
            print(
                "\n⚠️ No confident diagnosis could be made based on the provided symptoms.")
            print(
                "Consider providing more detailed information or consulting a healthcare professional.")


# Apply the question flow decorator
apply_question_flow(DermatologyExpert)
