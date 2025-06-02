from experta import *
from ExpertSystem.facts import Answer, question, Diagnosis, ImageDiagnosis, DiseaseInfo


class DermatologyExpert(KnowledgeEngine):

    @DefFacts()
    def initial_questions(self):
        yield DiseaseInfo(
            name="Eczema",
            common_symptoms={"itching": "high", "redness": "medium", "dryness": "high"},
            affected_gender="any",
            common_age_range="10-40",
            common_locations=["arms", "face"],
            severity_levels=["mild", "moderate", "severe"],
            common_duration="2 weeks",
            triggers=["stress", "allergens"],
            common_treatments=["moisturizers", "topical corticosteroids"],
            notes="Often flares up in dry or cold weather.",
        )
        yield DiseaseInfo(
            name="Psoriasis",
            common_symptoms={"scaling": "high", "redness": "high"},
            affected_gender="any",
            common_age_range="20-60",
            common_locations=["scalp", "elbows", "knees"],
            triggers=["stress", "infections"],
            common_treatments=["coal tar", "topical steroids"],
            notes="Chronic autoimmune condition.",
        )
        yield DiseaseInfo(
            name="Seborrheic Keratoses",
            common_symptoms={
                "waxy appearance": "high",
                "color change (brown/black)": "medium",
                "rough texture": "medium",
            },
            affected_gender="any",
            common_age_range="50+",
            common_locations=["chest", "back", "scalp", "face"],
            severity_levels=["mild"],
            common_duration="chronic",
            triggers=["aging", "genetics"],
            common_treatments=["cryotherapy", "curettage", "laser therapy"],
            notes="Non-cancerous; often mistaken for melanoma due to appearance.",
        )
        yield DiseaseInfo(
            name="Tinea (Ringworm)",
            common_symptoms={
                "itching": "high",
                "ring-shaped rash": "high",
                "scaly skin": "medium",
            },
            affected_gender="any",
            common_age_range="5-60",
            common_locations=["scalp", "feet", "groin", "body"],
            severity_levels=["mild", "moderate"],
            common_duration="2–4 weeks",
            triggers=["warm, moist environments", "skin contact", "shared items"],
            common_treatments=[
                "topical antifungals",
                "oral antifungals (severe cases)",
            ],
            notes="Highly contagious; different types named by location (e.g., tinea pedis = athlete’s foot).",
        )
        yield DiseaseInfo(
            name="Candidiasis",
            common_symptoms={
                "red rash": "high",
                "white patches (oral/vaginal)": "high",
                "itching or burning": "medium",
            },
            affected_gender="any",
            common_age_range="any",
            common_locations=["mouth", "groin", "skin folds", "vagina"],
            severity_levels=["mild", "moderate", "severe (immunocompromised)"],
            common_duration="1–2 weeks",
            triggers=["antibiotics", "diabetes", "immunosuppression", "moisture"],
            common_treatments=[
                "antifungal creams",
                "oral antifungals",
                "hygiene improvements",
            ],
            notes="Caused by Candida species, especially Candida albicans.",
        )
        yield DiseaseInfo(
            name="Tinea Versicolor",
            common_symptoms={
                "discolored patches": "high",
                "mild scaling": "medium",
                "slight itching": "low",
            },
            affected_gender="any",
            common_age_range="teenagers to young adults",
            common_locations=["trunk", "shoulders", "upper arms"],
            severity_levels=["mild"],
            common_duration="weeks to months",
            triggers=["humidity", "oily skin", "immunosuppression"],
            common_treatments=[
                "antifungal shampoos",
                "topical antifungals",
                "oral antifungals (persistent cases)",
            ],
            notes="Caused by yeast (Malassezia); more visible after sun exposure.",
        )
        yield DiseaseInfo(
            name="Onychomycosis",
            common_symptoms={
                "thickened nails": "high",
                "discoloration": "high",
                "brittle or crumbly nails": "medium",
            },
            affected_gender="any",
            common_age_range="40+",
            common_locations=["toenails", "fingernails"],
            severity_levels=["mild", "moderate", "severe"],
            common_duration="months",
            triggers=["tight shoes", "moisture", "trauma"],
            common_treatments=["oral antifungals", "medicated nail lacquers"],
            notes="Requires long treatment; recurrence is common.",
        )
        yield DiseaseInfo(
            name="Lipoma",
            common_symptoms={
                "soft lump under skin": "high",
                "slow growth": "high",
                "non-painful": "medium",
            },
            affected_gender="any",
            common_age_range="30-60",
            common_locations=["shoulders", "back", "neck", "arms"],
            severity_levels=["mild"],
            common_duration="chronic",
            triggers=["genetics"],
            common_treatments=["surgical excision", "liposuction"],
            notes="Benign fatty tumor; usually painless unless pressing on nerves.",
        )
        yield DiseaseInfo(
            name="Dermatofibroma",
            common_symptoms={
                "firm nodule": "high",
                "pigmentation": "medium",
                "dimpling when pinched": "medium",
            },
            affected_gender="more common in women",
            common_age_range="20-50",
            common_locations=["legs", "arms"],
            severity_levels=["mild"],
            common_duration="chronic",
            triggers=["minor skin injuries"],
            common_treatments=["surgical removal", "cryotherapy (rare)"],
            notes="Benign; may remain for years without causing harm.",
        )
        yield DiseaseInfo(
            name="Warts (Verruca Vulgaris)",
            common_symptoms={
                "rough raised bumps": "high",
                "flesh-colored or darker": "medium",
                "pain on pressure (plantar)": "low",
            },
            affected_gender="any",
            common_age_range="5-30",
            common_locations=["hands", "feet", "fingers", "knees"],
            severity_levels=["mild", "moderate"],
            common_duration="months to years",
            triggers=["HPV infection", "skin trauma", "weakened immunity"],
            common_treatments=["cryotherapy", "salicylic acid", "laser therapy"],
            notes="Caused by Human Papillomavirus (HPV); can spread through contact or shared surfaces.",
        )
        yield DiseaseInfo(
            name="Molluscum Contagiosum",
            common_symptoms={
                "pearly dome-shaped bumps": "high",
                "central dimple": "medium",
                "mild itching or redness": "low",
            },
            affected_gender="any",
            common_age_range="1-10 (children)",  # also adults with weakened immunity
            common_locations=["trunk", "arms", "groin", "face"],
            severity_levels=["mild"],
            common_duration="6–12 months (self-limited)",
            triggers=["skin-to-skin contact", "immunosuppression", "shared towels"],
            common_treatments=[
                "curettage",
                "cryotherapy",
                "topical agents (imiquimod)",
            ],
            notes="Viral infection by a poxvirus; often resolves on its own.",
        )
        yield DiseaseInfo(
            name="Herpes Simplex Virus (HSV)",
            common_symptoms={
                "painful blisters": "high",
                "tingling or burning before rash": "medium",
                "crusting sores": "medium",
            },
            affected_gender="any",
            common_age_range="15-50",
            common_locations=["lips", "genitals", "buttocks"],
            severity_levels=["mild", "moderate", "severe (immunocompromised)"],
            common_duration="7–14 days (per episode)",
            triggers=["stress", "illness", "sun exposure"],
            common_treatments=["acyclovir", "valacyclovir", "famciclovir"],
            notes="Recurrent viral infection; HSV-1 typically oral, HSV-2 genital.",
        )
        yield DiseaseInfo(
            name="Herpes Zoster (Shingles)",
            common_symptoms={
                "painful rash": "high",
                "blistering": "high",
                "burning or tingling": "high",
            },
            affected_gender="any",
            common_age_range="50+",
            common_locations=["torso", "face", "back"],
            severity_levels=["moderate", "severe"],
            common_duration="2–4 weeks",
            triggers=["previous chickenpox infection", "weakened immunity"],
            common_treatments=[
                "antivirals (acyclovir, valacyclovir)",
                "pain relievers",
            ],
            notes="Caused by reactivation of varicella-zoster virus; postherpetic neuralgia can follow.",
        )
        yield DiseaseInfo(
            name="Onychomycosis (Nail Fungus)",
            common_symptoms={
                "thickened nails": "high",
                "discoloration (yellow/white)": "high",
                "brittle or crumbly nails": "medium",
            },
            affected_gender="any",
            common_age_range="40+",
            common_locations=["toenails", "fingernails"],
            severity_levels=["mild", "moderate", "severe"],
            common_duration="months to years",
            triggers=["moisture", "tight footwear", "poor hygiene"],
            common_treatments=[
                "oral antifungals",
                "topical antifungals",
                "medicated nail lacquers",
            ],
            notes="Recurrence is common; long-term treatment often required.",
        )
        yield DiseaseInfo(
            name="Paronychia",
            common_symptoms={
                "swelling around nail": "high",
                "redness and tenderness": "high",
                "pus formation": "medium",
            },
            affected_gender="any",
            common_age_range="any",
            common_locations=["fingernails", "toenails"],
            severity_levels=["mild", "moderate"],
            common_duration="days to weeks (acute), months (chronic)",
            triggers=["nail biting", "manicures", "moisture exposure"],
            common_treatments=["warm soaks", "antibiotics", "drainage (if abscess)"],
            notes="Can be acute (bacterial) or chronic (fungal or mixed).",
        )
        yield DiseaseInfo(
            name="Nail Psoriasis",
            common_symptoms={
                "pitting": "high",
                "nail separation": "medium",
                "discoloration (oil spots)": "medium",
            },
            affected_gender="any",
            common_age_range="20-60",
            common_locations=["fingernails", "toenails"],
            severity_levels=["mild", "moderate", "severe"],
            common_duration="chronic",
            triggers=["psoriasis flare-ups", "trauma"],
            common_treatments=[
                "topical steroids",
                "systemic therapies (for psoriasis)",
                "nail protection",
            ],
            notes="Occurs in up to 50% of people with psoriasis.",
        )
        yield DiseaseInfo(
            name="Beau’s Lines",
            common_symptoms={"horizontal nail grooves": "high", "nail thinning": "low"},
            affected_gender="any",
            common_age_range="any",
            common_locations=["fingernails", "toenails"],
            severity_levels=["mild"],
            common_duration="weeks to months (depending on cause)",
            triggers=["severe illness", "trauma", "chemotherapy"],
            common_treatments=["treat underlying cause"],
            notes="Reflects temporary interruption of nail growth.",
        )
        yield DiseaseInfo(
            name="Koilonychia (Spoon Nails)",
            common_symptoms={
                "concave nail shape": "high",
                "thin, brittle nails": "medium",
            },
            affected_gender="any",
            common_age_range="children, adults with iron-deficiency anemia",
            common_locations=["fingernails"],
            severity_levels=["mild", "moderate"],
            common_duration="chronic unless treated",
            triggers=["iron deficiency", "genetic factors"],
            common_treatments=["iron supplementation", "diet correction"],
            notes="Often associated with anemia and systemic illness.",
        )
        yield DiseaseInfo(
            name="Atopic Dermatitis",
            common_symptoms={
                "itching": "high",
                "dry skin": "high",
                "redness and inflammation": "medium",
                "crusting or oozing": "low",
            },
            affected_gender="any",
            common_age_range="infancy to 30",
            common_locations=["face", "neck", "elbows", "knees", "hands"],
            severity_levels=["mild", "moderate", "severe"],
            common_duration="chronic with flares",
            triggers=[
                "allergens",
                "stress",
                "weather changes",
                "irritants (soaps, wool)",
            ],
            common_treatments=[
                "moisturizers",
                "topical corticosteroids",
                "calcineurin inhibitors",
                "antihistamines",
            ],
            notes="Often part of the “atopic triad” (with asthma and allergic rhinitis); worsens in dry environments.",
        )

        yield DiseaseInfo(
            name="Bullous Disease",
            common_symptoms={"blisters": "high", "pain": "medium"},
            affected_gender="any",
            common_age_range="50+",
            common_locations=["arms", "trunk", "legs"],
            severity_levels=["moderate", "severe"],
            common_duration="weeks to months",
            triggers=["autoimmune response"],
            common_treatments=["corticosteroids", "immunosuppressants"],
            notes="Autoimmune blistering diseases such as pemphigoid or pemphigus."
        )

        yield DiseaseInfo(
            name="Herpes / STDs",
            common_symptoms={"blisters": "high", "pain": "high"},
            affected_gender="any",
            common_age_range="15-45",
            common_locations=["genital area", "mouth", "buttocks"],
            severity_levels=["mild", "moderate"],
            common_duration="1-3 weeks (recurring)",
            triggers=["viral infection (HSV/HPV)", "sexual contact"],
            common_treatments=["antivirals (acyclovir)", "topical treatments"],
            notes="Painful fluid-filled blisters caused by sexually transmitted viruses."
        )

        yield DiseaseInfo(
            name="Systemic Disease",
            common_symptoms={"joint_pain": "medium", "rash_location": "variable"},
            affected_gender="any",
            common_age_range="20-60",
            common_locations=["face", "arms", "chest"],
            severity_levels=["mild", "severe"],
            common_duration="chronic",
            triggers=["autoimmune disorder"],
            common_treatments=["corticosteroids", "DMARDs", "immunotherapy"],
            notes="Internal diseases like lupus or vasculitis with skin symptoms."
        )

        yield DiseaseInfo(
            name="Vasculitis",
            common_symptoms={"ulcer": "medium", "pain": "medium"},
            affected_gender="any",
            common_age_range="30-70",
            common_locations=["legs", "feet", "fingers"],
            severity_levels=["moderate", "severe"],
            common_duration="weeks to chronic",
            triggers=["autoimmune response", "infections"],
            common_treatments=["corticosteroids", "immunosuppressants"],
            notes="Inflammation of blood vessels causing skin ulcers and pain."
        )

        yield DiseaseInfo(
            name="Malignant Skin Lesions",
            common_symptoms={"ulcer": "high", "discoloration": "high"},
            affected_gender="any",
            common_age_range="40+",
            common_locations=["face", "ears", "scalp", "hands"],
            severity_levels=["moderate", "severe"],
            common_duration="persistent / chronic",
            triggers=["UV radiation", "aging", "genetics"],
            common_treatments=["excision", "cryotherapy", "topical chemotherapy"],
            notes="Includes Actinic Keratosis and Basal Cell Carcinoma — can progress to skin cancer."
        )


        questions = [
            ("itching", "Is the skin itchy?"),
            ("dryness", "Is the skin dry or rough?"),
            ("scaling", "Is the skin scaly or flaky?"),
            ("redness", "Is the affected area red or inflamed?"),
            ("blisters", "Do you see any blisters or fluid-filled bumps?"),
            ("oozing_crusting", "Is there oozing or crusting on the skin?"),
            ("pain", "Is the skin painful to touch?"),
            ("discoloration", "Do you notice any change in skin color or pigment?"),
            ("hair_loss", "Have you experienced any patchy hair loss?"),
            ("nail_changes", "Do your nails appear thickened, brittle, or discolored?"),
            ("ulcer", "Do you have any non-healing ulcers or sores?"),
            ("photosensitivity", "Do symptoms worsen with sun exposure?"),
            ("warts", "Do you see warts or small rough bumps on the skin?"),
            ("hives", "Do you get raised, red, itchy welts (hives)?"),
            ("fever_rash", "Have you had a fever along with a skin rash?"),
            ("worse_at_night", "Is the itching worse at night?"),
            ("rash_shape", "Are the lesions ring-shaped or have a clear border?"),
            (
                "trigger_cosmetics",
                "Did the symptoms appear after using a cosmetic or cream?",
            ),
            ("joint_pain", "Do you have joint pain along with the rash?"),
            ("rash_between_fingers", "Is the rash between your fingers?"),
            ("rash_scalp", "Do you have flaking or redness on your scalp?"),
            ("bleeding", "Is the lesion bleeding spontaneously?"),
            ("enlarging_rapidly", "Has the lesion grown rapidly in size?"),
            ("crusting_scalp", "Is there crusting or scaling on your scalp?"),
            ("mucosal_involvement", "Are your lips, mouth or genitals also affected?"),
            ("sun_exposure_area", "Is the lesion in a sun-exposed area?"),
            ("history_cancer", "Do you have a personal or family history of cancer?"),
            ("recurrence", "Has the rash appeared in the same area before?")
        ]

        for ident, text in questions:
            yield question(ident=ident, text=text, valid=["yes", "no"], Type="multi")

        yield question(
            ident="rash_location",
            text="Where is the rash located?",
            valid=[],
            Type="text",
        )

    @Rule(
        Fact(next=MATCH.next_q),
        question(
            ident=MATCH.next_q, text=MATCH.text, valid=MATCH.valid, Type=MATCH.Type
        ),
        NOT(Answer(ident=MATCH.next_q)),
    )
    def ask_next_question(self, next_q, text, valid, Type):
        # Check if diagnosis already exists
        for fact in self.facts.values():
            if isinstance(fact, Diagnosis):
                # Skip asking if diagnosis is already made
                return

        response = self.ask_user(text, Type, valid)
        cf = 1.0 if response == "yes" else 0.0
        self.declare(Answer(ident=next_q, text=response, cf=cf))


    def ask_user(self, question_text, Type, valid=None):
        print("\n🧠 " + question_text)
        if Type == "multi" and valid:
            print(f"Valid responses: {', '.join(valid)}")
        response = input("Your answer: ").strip().lower()
        return response

    # Fixed rule flow - now properly chains questions
    @Rule(Answer(ident="itching", text="yes"))
    def itching_yes(self):
        self.declare(Fact(next="dryness"))

    @Rule(Answer(ident="itching", text="no"))
    def itching_no(self):
        self.declare(Fact(next="scaling"))

    @Rule(Answer(ident="dryness", text="yes"))
    def dryness_yes(self):
        self.declare(Fact(next="redness"))

    @Rule(Answer(ident="dryness", text="no"))
    def dryness_no(self):
        self.declare(Fact(next="scaling"))

    @Rule(Answer(ident="scaling", text="yes"))
    def scaling_yes(self):
        self.declare(Fact(next="redness"))

    @Rule(Answer(ident="scaling", text="no"))
    def scaling_no(self):
        self.declare(Fact(next="redness"))

    # Add rule to continue after redness question
    @Rule(Answer(ident="redness", text=MATCH.response))
    def redness_answered(self, response):
        # Continue with more questions or end diagnosis
        self.declare(Fact(next="blisters"))
    
    @Rule(Answer(ident="blisters", text=MATCH.response))
    def after_blisters(self, response):
        self.declare(Fact(next="pain"))


    @Rule(Answer(ident="pain", text=MATCH.response))
    def after_pain(self, response):
        self.declare(Fact(next="ulcer"))


    @Rule(Answer(ident="ulcer", text=MATCH.response))
    def after_ulcer(self, response):
        self.declare(Fact(next="discoloration"))


    @Rule(Answer(ident="discoloration", text=MATCH.response))
    def after_discoloration(self, response):
        self.declare(Fact(next="joint_pain"))


    @Rule(Answer(ident="joint_pain", text=MATCH.response))
    def after_joint_pain(self, response):
        self.declare(Fact(next="bleeding"))


    @Rule(Answer(ident="bleeding", text=MATCH.response))
    def after_bleeding(self, response):
        self.declare(Fact(next="enlarging_rapidly"))


    @Rule(Answer(ident="enlarging_rapidly", text=MATCH.response))
    def after_enlarging(self, response):
        self.declare(Fact(next="mucosal_involvement"))


    @Rule(Answer(ident="mucosal_involvement", text=MATCH.response))
    def after_mucosal(self, response):
        self.declare(Fact(next="sun_exposure_area"))


    def combine_cf(self, cf1, cf2):
        if cf1 >= 0 and cf2 >= 0:
            return cf1 + cf2 * (1 - cf1)
        elif cf1 < 0 and cf2 < 0:
            return cf1 + cf2 * (1 + cf1)
        else:
            return (cf1 + cf2) / (1 - min(abs(cf1), abs(cf2)))

    def declare_or_update_diagnosis(self, disease, reasoning, new_cf):
        found = None
        for fact in self.facts.values():
            if isinstance(fact, Diagnosis) and fact["disease"] == disease:
                found = fact
                break
        if found:
            combined_cf = self.combine_cf(found["cf"], new_cf)
            self.modify(
                found,
                cf=combined_cf,
                reasoning=reasoning + f" (updated CF: {combined_cf:.2f})",
            )
        else:
            self.declare(Diagnosis(disease=disease, reasoning=reasoning, cf=new_cf))

    # Fixed diagnosis rules with proper logic
    @Rule(
        DiseaseInfo(name="Eczema", common_symptoms=MATCH.symptoms),
        Answer(ident="itching", text="yes", cf=MATCH.cf1),
        Answer(ident="dryness", text="yes", cf=MATCH.cf2),
        TEST(lambda symptoms: "dryness" in symptoms and symptoms["dryness"] == "high"),
    )
    def diagnose_eczema_comprehensive(self, cf1, cf2, symptoms):
        combined_cf = self.combine_cf(cf1, cf2)
        self.declare_or_update_diagnosis(
            disease="Eczema",
            reasoning=f"Itching and dryness are high-weight symptoms for Eczema. Itching intensity: {symptoms['itching']}, Dryness intensity: {symptoms['dryness']}",
            new_cf=combined_cf * 0.9,
        )

    @Rule(
        Answer(ident="itching", text="yes", cf=MATCH.cf1),
        Answer(ident="dryness", text="yes", cf=MATCH.cf2),
    )
    def diagnose_eczema_simple(self, cf1, cf2):
        combined_cf = self.combine_cf(cf1, cf2)
        self.declare_or_update_diagnosis(
            disease="Eczema",
            reasoning="Patient reports itching and dryness, common in eczema",
            new_cf=combined_cf * 0.7,
        )

    @Rule(
        DiseaseInfo(name="Psoriasis", common_symptoms=MATCH.symptoms),
        Answer(ident="scaling", text="yes", cf=MATCH.cf1),
        Answer(ident="redness", text="yes", cf=MATCH.cf2),
        TEST(lambda symptoms: "scaling" in symptoms and "redness" in symptoms),
    )
    def diagnose_psoriasis_comprehensive(self, cf1, cf2, symptoms):
        combined_cf = self.combine_cf(cf1, cf2)
        self.declare_or_update_diagnosis(
            disease="Psoriasis",
            reasoning=f"Scaling and redness match Psoriasis profile. Scaling intensity: {symptoms['scaling']}, Redness intensity: {symptoms['redness']}",
            new_cf=combined_cf * 0.85,
        )

    @Rule(
        Answer(ident="scaling", text="yes", cf=MATCH.cf1),
        Answer(ident="redness", text="yes", cf=MATCH.cf2),
    )
    def diagnose_psoriasis_simple(self, cf1, cf2):
        combined_cf = self.combine_cf(cf1, cf2)
        self.declare_or_update_diagnosis(
            disease="Psoriasis",
            reasoning="Patient reports scaling and redness, characteristic of psoriasis",
            new_cf=combined_cf * 0.75,
        )

    @Rule(
        ImageDiagnosis(disease="Eczema", confidence=MATCH.conf),
        TEST(lambda conf: conf >= 0.7),
    )
    def diagnose_eczema_cv(self, conf):
        self.declare_or_update_diagnosis(
            "Eczema",
            f"Computer vision predicted Eczema with {conf:.2f} confidence",
            new_cf=conf,
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
            "Malignant Lesion (Skin Cancer)",
            f"CV model predicted malignancy with {conf:.2f} confidence",
            new_cf=conf
        )


    # Add a rule to trigger final diagnosis after collecting enough information
    @Rule(
        Answer(ident="redness", text=MATCH.response), salience=-10
    )  # Lower priority to run after other rules
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
            print(f"\n✅ Diagnosis: {final['disease']}")
            print(f"Reason: {final['reasoning']}")
            print(f"Confidence: {final['cf']*100:.1f}%")
        else:
            print("\n⚠️ No confident diagnosis made.")
            print(
                "Consider providing more symptoms or consulting a healthcare professional."
            )
