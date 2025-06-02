from experta import *
from ExpertSystem.facts import Answer, question, Diagnosis, ImageDiagnosis, DiseaseInfo


class DermatologyExpert(KnowledgeEngine):

    @DefFacts()
    def initial_questions(self):
        yield DiseaseInfo(
            name='Eczema',
            common_symptoms={'itching': 'high',
                             'redness': 'medium', 'dryness': 'high'},
            affected_gender='any',
            common_age_range='10-40',
            common_locations=['arms', 'face'],
            severity_levels=['mild', 'moderate', 'severe'],
            common_duration='2 weeks',
            triggers=['stress', 'allergens'],
            common_treatments=['moisturizers', 'topical corticosteroids'],
            notes='Often flares up in dry or cold weather.'
        )
        yield DiseaseInfo(
            name='Psoriasis',
            common_symptoms={'scaling': 'high', 'redness': 'high'},
            affected_gender='any',
            common_age_range='20-60',
            common_locations=['scalp', 'elbows', 'knees'],
            triggers=['stress', 'infections'],
            common_treatments=['coal tar', 'topical steroids'],
            notes='Chronic autoimmune condition.'
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
            ("trigger_cosmetics",
             "Did the symptoms appear after using a cosmetic or cream?"),
            ("joint_pain", "Do you have joint pain along with the rash?"),
            ("rash_between_fingers", "Is the rash between your fingers?"),
            ("rash_scalp", "Do you have flaking or redness on your scalp?")
        ]

        for ident, text in questions:
            yield question(ident=ident, text=text, valid=["yes", "no"], Type="multi")

        yield question(ident="rash_location", text="Where is the rash located?", valid=[], Type="text")

    @Rule(Fact(next=MATCH.next_q),
          question(ident=MATCH.next_q, text=MATCH.text,
                   valid=MATCH.valid, Type=MATCH.Type),
          NOT(Answer(ident=MATCH.next_q)))
    def ask_next_question(self, next_q, text, valid, Type):
        response = self.ask_user(text, Type, valid)
        cf = 1.0 if response == "yes" else 0.0
        self.declare(Answer(ident=next_q, text=response, cf=cf))

    def ask_user(self, question_text, Type, valid=None):
        print("\n🧠 " + question_text)
        if Type == "multi" and valid:
            print(f"Valid responses: {', '.join(valid)}")
        response = input("Your answer: ").strip().lower()
        return response

    @Rule(Answer(ident='itching', text='yes'))
    def itching_yes(self):
        self.declare(Fact(next='dryness'))

    @Rule(Answer(ident='itching', text='no'))
    def itching_no(self):
        self.declare(Fact(next='scaling'))

    @Rule(Answer(ident='dryness', text='yes'))
    def dryness_yes(self):
        self.declare(Fact(next='redness'))

    @Rule(Answer(ident='dryness', text='no'))
    def dryness_no(self):
        self.declare(Fact(next='scaling'))

    @Rule(Answer(ident='scaling', text='yes'))
    def scaling_yes(self):
        self.declare(Fact(next='redness'))

    @Rule(Answer(ident='scaling', text='no'))
    def scaling_no(self):
        self.declare(Fact(next='redness'))

    @Rule(Answer(ident='redness', text=MATCH.response))
    def redness_answered(self, response):
        self.declare(Fact(next='blisters'))

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
            if isinstance(fact, Diagnosis) and fact['disease'] == disease:
                found = fact
                break
        if found:
            combined_cf = self.combine_cf(found['cf'], new_cf)
            self.modify(found, cf=combined_cf, reasoning=reasoning +
                        f" (updated CF: {combined_cf:.2f})")
        else:
            self.declare(Diagnosis(disease=disease,
                         reasoning=reasoning, cf=new_cf))

    @Rule(DiseaseInfo(name='Eczema', common_symptoms=MATCH.symptoms),
          Answer(ident='itching', text='yes', cf=MATCH.cf1),
          Answer(ident='dryness', text='yes', cf=MATCH.cf2),
          TEST(lambda symptoms: 'dryness' in symptoms and symptoms['dryness'] == 'high'))
    def diagnose_eczema_comprehensive(self, cf1, cf2, symptoms):
        combined_cf = self.combine_cf(cf1, cf2)
        self.declare_or_update_diagnosis(
            disease="Eczema",
            reasoning=f"Itching and dryness are high-weight symptoms for Eczema. Itching intensity: {symptoms['itching']}, Dryness intensity: {symptoms['dryness']}",
            new_cf=combined_cf * 0.9
        )

    @Rule(Answer(ident='itching', text='yes', cf=MATCH.cf1),
          Answer(ident='dryness', text='yes', cf=MATCH.cf2))
    def diagnose_eczema_simple(self, cf1, cf2):
        combined_cf = self.combine_cf(cf1, cf2)
        self.declare_or_update_diagnosis(
            disease="Eczema",
            reasoning="Patient reports itching and dryness, common in eczema",
            new_cf=combined_cf * 0.7
        )

    @Rule(DiseaseInfo(name='Psoriasis', common_symptoms=MATCH.symptoms),
          Answer(ident='scaling', text='yes', cf=MATCH.cf1),
          Answer(ident='redness', text='yes', cf=MATCH.cf2),
          TEST(lambda symptoms: 'scaling' in symptoms and 'redness' in symptoms))
    def diagnose_psoriasis_comprehensive(self, cf1, cf2, symptoms):
        combined_cf = self.combine_cf(cf1, cf2)
        self.declare_or_update_diagnosis(
            disease="Psoriasis",
            reasoning=f"Scaling and redness match Psoriasis profile. Scaling intensity: {symptoms['scaling']}, Redness intensity: {symptoms['redness']}",
            new_cf=combined_cf * 0.85
        )

    @Rule(Answer(ident='scaling', text='yes', cf=MATCH.cf1),
          Answer(ident='redness', text='yes', cf=MATCH.cf2))
    def diagnose_psoriasis_simple(self, cf1, cf2):
        combined_cf = self.combine_cf(cf1, cf2)
        self.declare_or_update_diagnosis(
            disease="Psoriasis",
            reasoning="Patient reports scaling and redness, characteristic of psoriasis",
            new_cf=combined_cf * 0.75
        )

    @Rule(ImageDiagnosis(disease='Eczema', confidence=MATCH.conf),
          TEST(lambda conf: conf >= 0.7))
    def diagnose_eczema_cv(self, conf):
        self.declare_or_update_diagnosis(
            "Eczema",
            f"Computer vision predicted Eczema with {conf:.2f} confidence",
            new_cf=conf
        )

    @Rule(Answer(ident='redness', text=MATCH.response),
          salience=-10)  
    def trigger_final_diagnosis(self, response):
        self.declare(Fact(diagnosis_ready=True))

    def get_final_diagnosis(self):
        final = None
        best_cf = -1.0
        for fact in self.facts.values():
            if isinstance(fact, Diagnosis) and fact['cf'] > best_cf:
                final = fact
                best_cf = fact['cf']
        if final:
            print(f"\n✅ Diagnosis: {final['disease']}")
            print(f"Reason: {final['reasoning']}")
            print(f"Confidence: {final['cf']*100:.1f}%")
        else:
            print("\n⚠️ No confident diagnosis made.")
            print(
                "Consider providing more symptoms or consulting a healthcare professional.")


