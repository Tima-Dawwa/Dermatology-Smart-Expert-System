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

    @Rule(DiseaseInfo(name="Eczema", common_symptoms=MATCH.symptoms),
          Answer(ident="itching", text="yes", cf=MATCH.cf1),
          Answer(ident="dryness", text="yes", cf=MATCH.cf2),
          TEST(lambda symptoms: "dryness" in symptoms and symptoms["dryness"] == "high"))
    def diagnose_eczema_comprehensive(self, cf1, cf2, symptoms):
        cf = self.combine_cf(cf1, cf2)
        self.declare_or_update_diagnosis(
            disease="Eczema",
            reasoning="Itching and dryness are high-weight symptoms for Eczema.",
            new_cf=cf * 0.9
        )

    @Rule(Answer(ident="itching", text="yes", cf=MATCH.cf1),
          Answer(ident="dryness", text="yes", cf=MATCH.cf2))
    def diagnose_eczema_simple(self, cf1, cf2):
        cf = self.combine_cf(cf1, cf2)
        self.declare_or_update_diagnosis(
            disease="Eczema",
            reasoning="Patient reports itching and dryness, common in eczema.",
            new_cf=cf * 0.7
        )

    @Rule(DiseaseInfo(name="Psoriasis", common_symptoms=MATCH.symptoms),
          Answer(ident="scaling", text="yes", cf=MATCH.cf1),
          Answer(ident="redness", text="yes", cf=MATCH.cf2),
          TEST(lambda symptoms: "scaling" in symptoms and "redness" in symptoms))
    def diagnose_psoriasis_comprehensive(self, cf1, cf2, symptoms):
        cf = self.combine_cf(cf1, cf2)
        self.declare_or_update_diagnosis(
            disease="Psoriasis",
            reasoning="Scaling and redness match Psoriasis profile.",
            new_cf=cf * 0.85
        )

    @Rule(Answer(ident="scaling", text="yes", cf=MATCH.cf1),
          Answer(ident="redness", text="yes", cf=MATCH.cf2))
    def diagnose_psoriasis_simple(self, cf1, cf2):
        cf = self.combine_cf(cf1, cf2)
        self.declare_or_update_diagnosis(
            disease="Psoriasis",
            reasoning="Patient reports scaling and redness, characteristic of psoriasis.",
            new_cf=cf * 0.75
        )

    @Rule(ImageDiagnosis(disease="Eczema", confidence=MATCH.conf),
          TEST(lambda conf: conf >= 0.7))
    def diagnose_eczema_cv(self, conf):
        self.declare_or_update_diagnosis(
            disease="Eczema",
            reasoning=f"Computer vision predicted Eczema with {conf:.2f} confidence.",
            new_cf=conf
        )

    @Rule(Answer(ident="blisters", text="yes", cf=MATCH.cf1),
          Answer(ident="pain", text="yes", cf=MATCH.cf2))
    def diagnose_bullous_disease(self, cf1, cf2):
        cf = self.combine_cf(cf1, cf2)
        self.declare_or_update_diagnosis(
            disease="Bullous Disease",
            reasoning="Blisters with pain suggest bullous autoimmune condition.",
            new_cf=cf * 0.85
        )

    @Rule(Answer(ident="mucosal_involvement", text="yes", cf=MATCH.cf1),
          Answer(ident="blisters", text="yes", cf=MATCH.cf2))
    def diagnose_herpes_stds(self, cf1, cf2):
        cf = self.combine_cf(cf1, cf2)
        self.declare_or_update_diagnosis(
            disease="Herpes or STD",
            reasoning="Blisters affecting mucosal areas suggest HSV or similar STD.",
            new_cf=cf * 0.9
        )

    @Rule(Answer(ident="joint_pain", text="yes", cf=MATCH.cf1),
          Answer(ident="photosensitivity", text="yes", cf=MATCH.cf2))
    def diagnose_systemic_disease(self, cf1, cf2):
        cf = self.combine_cf(cf1, cf2)
        self.declare_or_update_diagnosis(
            disease="Systemic Disease",
            reasoning="Joint pain with photosensitivity suggests autoimmune systemic disease.",
            new_cf=cf * 0.8
        )

    @Rule(Answer(ident="ulcer", text="yes", cf=MATCH.cf1),
          Answer(ident="discoloration", text="yes", cf=MATCH.cf2))
    def diagnose_vasculitis(self, cf1, cf2):
        cf = self.combine_cf(cf1, cf2)
        self.declare_or_update_diagnosis(
            disease="Vasculitis",
            reasoning="Non-healing ulcers with discoloration suggest skin vasculitis.",
            new_cf=cf * 0.85
        )

    @Rule(Answer(ident="bleeding", text="yes", cf=MATCH.cf1),
          Answer(ident="enlarging_rapidly", text="yes", cf=MATCH.cf2),
          Answer(ident="sun_exposure_area", text="yes", cf=MATCH.cf3))
    def diagnose_malignant_lesion(self, cf1, cf2, cf3):
        cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
        self.declare_or_update_diagnosis(
            disease="Malignant Lesion (Skin Cancer)",
            reasoning="Lesion is bleeding, enlarging rapidly, and in sun-exposed area — likely skin cancer.",
            new_cf=cf * 0.95
        )

    @Rule(ImageDiagnosis(disease="Malignant Lesion (Skin Cancer)", confidence=MATCH.conf),
          TEST(lambda conf: conf >= 0.7))
    def diagnose_cancer_cv(self, conf):
        self.declare_or_update_diagnosis(
            disease="Malignant Lesion (Skin Cancer)",
            reasoning=f"CV model predicted malignancy with {conf:.2f} confidence.",
            new_cf=conf
        )

    @Rule(Answer(ident="acne", text="yes", cf=MATCH.cf1),
          Answer(ident="rosacea", text="yes", cf=MATCH.cf2))
    def diagnose_acne_rosacea(self, cf1, cf2):
        cf = self.combine_cf(cf1, cf2)
        self.declare_or_update_diagnosis(
            disease="Acne and Rosacea",
            reasoning="Presence of pimples/blackheads and facial redness indicates Acne or Rosacea.",
            new_cf=cf * 0.85
        )

    @Rule(Answer(ident="hair_loss", text="yes", cf=MATCH.cf1))
    def diagnose_hair_loss(self, cf1):
        self.declare_or_update_diagnosis(
            disease="Hair Loss, Alopecia, and other Hair Diseases",
            reasoning="Hair loss or thinning is a key sign of hair diseases.",
            new_cf=cf1 * 0.85
        )

    @Rule(Answer(ident="rash_symmetry", text="yes", cf=MATCH.cf1),
          Answer(ident="drug_history", text="yes", cf=MATCH.cf2))
    def diagnose_drug_eruption(self, cf1, cf2):
        cf = self.combine_cf(cf1, cf2)
        self.declare_or_update_diagnosis(
            disease="Exanthems and Drug Eruptions",
            reasoning="Symmetrical rash and recent medication use suggest a drug eruption.",
            new_cf=cf * 0.9
        )

    @Rule(Answer(ident="itching", text="yes", cf=MATCH.cf1),
          Answer(ident="vesicles", text="yes", cf=MATCH.cf2),
          Answer(ident="contact_history", text="yes", cf=MATCH.cf3))
    def diagnose_contact_dermatitis(self, cf1, cf2, cf3):
        cf = self.combine_cf(cf1, self.combine_cf(cf2, cf3))
        self.declare_or_update_diagnosis(
            disease="Poison Ivy and other Contact Dermatitis",
            reasoning="Itching, vesicles, and contact history suggest contact dermatitis.",
            new_cf=cf * 0.9
        )

    @Rule(Answer(ident="sun_exposure_area", text="yes", cf=MATCH.cf1),
          Answer(ident="skin_lightening", text="yes", cf=MATCH.cf2))
    def diagnose_light_diseases(self, cf1, cf2):
        cf = self.combine_cf(cf1, cf2)
        self.declare_or_update_diagnosis(
            disease="Light Diseases and Disorders of Pigmentation",
            reasoning="Photosensitivity and skin lightening suggest a light-related disorder.",
            new_cf=cf * 0.85
        )

    @Rule(Answer(ident="redness", text=MATCH.response), salience=-10)
    def trigger_final_diagnosis(self, response):
        self.declare(Fact(diagnosis_ready=True))

    def get_final_diagnosis(self):
        final = None
        best_cf = -1.0
        for fact in self.facts.values():
            if isinstance(fact, Diagnosis) and fact["cf"] > best_cf:
                final = fact
                best_cf = fact["cf"]
        if final:
            print(f"\n\u2705 Diagnosis: {final['disease']}")
            print(f"Reason: {final['reasoning']}")
            print(f"Confidence: {final['cf'] * 100:.1f}%")
        else:
            print("\n\u26a0\ufe0f No confident diagnosis made.")
            print(
                "Consider providing more symptoms or consulting a healthcare professional.")


apply_question_flow(DermatologyExpert)
