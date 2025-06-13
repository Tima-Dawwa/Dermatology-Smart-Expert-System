from experta import *
from ExpertSystem.facts import Answer, NextQuestion


def apply_question_flow(cls):
    """
    This function contains all the rules for asking questions and applies them
    to the provided KnowledgeEngine class. It perfectly follows the decision tree.
    """

    # Add this new rule at the beginning of the function
    @Rule(Fact(start=True), salience=103)
    def ask_age(self):
        self.declare(NextQuestion(ident='age'))
    cls.ask_age = ask_age

    @Rule(Answer(ident='age'), NOT(Answer(ident='duration')), salience=102)
    def ask_duration(self):
        self.declare(NextQuestion(ident='duration'))
    cls.ask_duration = ask_duration

    @Rule(Answer(ident='duration'), NOT(Answer(ident='severity')), salience=101)
    def ask_severity(self):
        self.declare(NextQuestion(ident='severity'))
    cls.ask_severity = ask_severity

    # --- Step 1: Triage ---
    @Rule(Answer(ident='severity'), NOT(Answer(ident='has_symptom_lump_or_growth')), salience=100)
    def ask_triage_1(self):
        self.declare(NextQuestion(ident='has_symptom_lump_or_growth'))
    cls.ask_triage_1 = ask_triage_1

    @Rule(Answer(ident='has_symptom_lump_or_growth', text='no'), NOT(Answer(ident='affects_nails_or_hair')), salience=99)
    def ask_triage_2(self):
        self.declare(NextQuestion(ident='affects_nails_or_hair'))
    cls.ask_triage_2 = ask_triage_2

    @Rule(Answer(ident='has_symptom_lump_or_growth', text='no'), Answer(ident='affects_nails_or_hair', text='no'), NOT(Answer(ident='has_symptom_rash')), salience=98)
    def ask_triage_3(self):
        self.declare(NextQuestion(ident='has_symptom_rash'))
    cls.ask_triage_3 = ask_triage_3

    @Rule(OR(Answer(ident='has_symptom_rash', text='yes'),
             Answer(ident='has_symptom_lump_or_growth', text='yes')),
          NOT(Answer(ident='locations')),
          salience=97)
    def ask_location(self):
        self.declare(NextQuestion(ident='locations'))
    cls.ask_location = ask_location

    @Rule(Answer(ident='has_symptom_lump_or_growth', text='no'), Answer(ident='affects_nails_or_hair', text='no'), Answer(ident='has_symptom_rash', text='no'), NOT(Answer(ident='has_symptom_palpable_purpura')), salience=97)
    def ask_triage_4_branch_d(self):
        self.declare(NextQuestion(ident='has_symptom_palpable_purpura'))
    cls.ask_triage_4_branch_d = ask_triage_4_branch_d

    # --- Branch A: Growths ---

    @Rule(Answer(ident='has_symptom_lump_or_growth', text='yes'), NOT(Answer(ident='has_symptom_soft_lump')), salience=90)
    def ask_a1(self): self.declare(NextQuestion(ident='has_symptom_soft_lump'))
    cls.ask_a1 = ask_a1

    @Rule(Answer(ident='has_symptom_lump_or_growth', text='yes'), Answer(ident='has_symptom_soft_lump', text='no'), NOT(Answer(ident='has_symptom_firm_lump')), salience=89)
    def ask_a2(self): self.declare(NextQuestion(ident='has_symptom_firm_lump'))
    cls.ask_a2 = ask_a2

    @Rule(Answer(ident='has_symptom_lump_or_growth', text='yes'), Answer(ident='has_symptom_soft_lump', text='no'), Answer(ident='has_symptom_firm_lump', text='no'), NOT(Answer(ident='has_symptom_rough_bumps')), salience=88)
    def ask_a3(self): self.declare(
        NextQuestion(ident='has_symptom_rough_bumps'))
    cls.ask_a3 = ask_a3

    @Rule(Answer(ident='has_symptom_lump_or_growth', text='yes'), Answer(ident='has_symptom_soft_lump', text='no'), Answer(ident='has_symptom_firm_lump', text='no'), Answer(ident='has_symptom_rough_bumps', text='no'), NOT(Answer(ident='has_symptom_waxy_appearance')), salience=87)
    def ask_a5(self): self.declare(
        NextQuestion(ident='has_symptom_waxy_appearance'))
    cls.ask_a5 = ask_a5

    @Rule(Answer(ident='has_symptom_lump_or_growth', text='yes'), Answer(ident='has_symptom_soft_lump', text='no'), Answer(ident='has_symptom_firm_lump', text='no'), Answer(ident='has_symptom_rough_bumps', text='no'), Answer(ident='has_symptom_waxy_appearance', text='no'), NOT(Answer(ident='has_symptom_evolution_of_mole')), salience=86)
    def ask_a6(self): self.declare(NextQuestion(
        ident='has_symptom_evolution_of_mole'))
    cls.ask_a6 = ask_a6

    @Rule(Answer(ident='has_symptom_lump_or_growth', text='yes'), Answer(ident='has_symptom_soft_lump', text='no'), Answer(ident='has_symptom_firm_lump', text='no'), Answer(ident='has_symptom_rough_bumps', text='no'), Answer(ident='has_symptom_waxy_appearance', text='no'), Answer(ident='has_symptom_evolution_of_mole', text='no'), NOT(Answer(ident='has_symptom_sore_that_wont_heal')), salience=85)
    def ask_a7(self): self.declare(NextQuestion(
        ident='has_symptom_sore_that_wont_heal'))
    cls.ask_a7 = ask_a7

    @Rule(Answer(ident='has_symptom_sore_that_wont_heal', text='yes'), NOT(Answer(ident='has_symptom_persistent_scaly_patch')), salience=83)
    def ask_a7_followup1(self): self.declare(
        NextQuestion(ident='has_symptom_persistent_scaly_patch'))
    cls.ask_a7_followup1 = ask_a7_followup1

    # --- Branch B: Hair & Nails ---

    @Rule(Answer(ident='affects_nails_or_hair', text='yes'), NOT(Answer(ident='has_symptom_patchy_hair_loss')), salience=90)
    def ask_b1(self): self.declare(NextQuestion(
        ident='has_symptom_patchy_hair_loss'))
    cls.ask_b1 = ask_b1

    @Rule(Answer(ident='affects_nails_or_hair', text='yes'), Answer(ident='has_symptom_patchy_hair_loss', text='no'), NOT(Answer(ident='has_symptom_nail_pitting')), salience=89)
    def ask_b2(self): self.declare(
        NextQuestion(ident='has_symptom_nail_pitting'))
    cls.ask_b2 = ask_b2

    @Rule(Answer(ident='affects_nails_or_hair', text='yes'), Answer(ident='has_symptom_patchy_hair_loss', text='no'), Answer(ident='has_symptom_nail_pitting', text='no'), NOT(Answer(ident='has_symptom_nail_thickening')), salience=88)
    def ask_b3(self): self.declare(
        NextQuestion(ident='has_symptom_nail_thickening'))
    cls.ask_b3 = ask_b3

    @Rule(Answer(ident='affects_nails_or_hair', text='yes'), Answer(ident='has_symptom_patchy_hair_loss', text='no'), Answer(ident='has_symptom_nail_pitting', text='no'), Answer(ident='has_symptom_nail_thickening', text='no'), NOT(Answer(ident='has_symptom_nail_concavity')), salience=87)
    def ask_b4(self): self.declare(
        NextQuestion(ident='has_symptom_nail_concavity'))
    cls.ask_b4 = ask_b4

    @Rule(Answer(ident='affects_nails_or_hair', text='yes'), Answer(ident='has_symptom_patchy_hair_loss', text='no'), Answer(ident='has_symptom_nail_pitting', text='no'), Answer(ident='has_symptom_nail_thickening', text='no'), Answer(ident='has_symptom_nail_concavity', text='no'), NOT(Answer(ident='has_symptom_nail_fold_swelling')), salience=86)
    def ask_b5(self): self.declare(NextQuestion(
        ident='has_symptom_nail_fold_swelling'))
    cls.ask_b5 = ask_b5

    @Rule(Answer(ident='affects_nails_or_hair', text='yes'), Answer(ident='has_symptom_patchy_hair_loss', text='no'), Answer(ident='has_symptom_nail_pitting', text='no'), Answer(ident='has_symptom_nail_thickening', text='no'), Answer(ident='has_symptom_nail_concavity', text='no'), Answer(ident='has_symptom_nail_fold_swelling', text='no'), NOT(Answer(ident='has_symptom_transverse_nail_grooves')), salience=85)
    def ask_b6(self): self.declare(NextQuestion(
        ident='has_symptom_transverse_nail_grooves'))
    cls.ask_b6 = ask_b6

    # --- Branch C: Rashes ---
    @Rule(Answer(ident='has_symptom_rash', text='yes'), NOT(Answer(ident='has_symptom_itching')), salience=90)
    def ask_c_itch_test(self): self.declare(
        NextQuestion(ident='has_symptom_itching'))
    cls.ask_c_itch_test = ask_c_itch_test

    # --- Sub-Branch C.2: Itchy Rashes ---
    @Rule(Answer(ident='has_symptom_rash', text='yes'), Answer(ident='has_symptom_itching', text='yes'), NOT(Answer(ident='has_symptom_worse_at_night')), salience=80)
    def ask_c2_1(self): self.declare(
        NextQuestion(ident='has_symptom_worse_at_night'))
    cls.ask_c2_1 = ask_c2_1

    @Rule(Answer(ident='has_symptom_rash', text='yes'), Answer(ident='has_symptom_itching', text='yes'), Answer(ident='has_symptom_worse_at_night', text='no'), NOT(Answer(ident='has_symptom_dryness')), salience=79)
    def ask_c2_2(self): self.declare(NextQuestion(ident='has_symptom_dryness'))
    cls.ask_c2_2 = ask_c2_2

    @Rule(Answer(ident='has_symptom_rash', text='yes'), Answer(ident='has_symptom_itching', text='yes'), Answer(ident='has_symptom_worse_at_night', text='no'), Answer(ident='has_symptom_dryness', text='no'), NOT(Answer(ident='has_symptom_ring_shaped_rash')), salience=78)
    def ask_c2_3(self): self.declare(
        NextQuestion(ident='has_symptom_ring_shaped_rash'))
    cls.ask_c2_3 = ask_c2_3

    @Rule(Answer(ident='has_symptom_rash', text='yes'), Answer(ident='has_symptom_itching', text='yes'), Answer(ident='has_symptom_worse_at_night', text='no'), Answer(ident='has_symptom_dryness', text='no'), Answer(ident='has_symptom_ring_shaped_rash', text='no'), NOT(Answer(ident='has_symptom_white_patches')), salience=77)
    def ask_c2_4(self): self.declare(
        NextQuestion(ident='has_symptom_white_patches'))
    cls.ask_c2_4 = ask_c2_4

    @Rule(Answer(ident='has_symptom_rash', text='yes'), Answer(ident='has_symptom_itching', text='yes'), Answer(ident='has_symptom_worse_at_night', text='no'), Answer(ident='has_symptom_dryness', text='no'), Answer(ident='has_symptom_ring_shaped_rash', text='no'), Answer(ident='has_symptom_white_patches', text='no'), NOT(Answer(ident='has_symptom_blisters')), salience=76)
    def ask_c2_5_blisters(self): self.declare(
        NextQuestion(ident='has_symptom_blisters'))
    cls.ask_c2_5_blisters = ask_c2_5_blisters

    @Rule(Answer(ident='has_symptom_blisters', text='yes'), NOT(Answer(ident='trigger_contact_related')), salience=75)
    def ask_c2_5_contact(self): self.declare(
        NextQuestion(ident='trigger_contact_related'))
    cls.ask_c2_5_contact = ask_c2_5_contact

    @Rule(Answer(ident='has_symptom_blisters', text='yes'), Answer(ident='trigger_contact_related', text='no'), NOT(Answer(ident='has_symptom_large_tense_blisters')), salience=74)
    def ask_c2_5_tense(self): self.declare(
        NextQuestion(ident='has_symptom_large_tense_blisters'))
    cls.ask_c2_5_tense = ask_c2_5_tense

    @Rule(Answer(ident='has_symptom_rash', text='yes'), Answer(ident='has_symptom_itching', text='yes'), Answer(ident='has_symptom_worse_at_night', text='no'), Answer(ident='has_symptom_dryness', text='no'), Answer(ident='has_symptom_ring_shaped_rash', text='no'), Answer(ident='has_symptom_white_patches', text='no'), Answer(ident='has_symptom_blisters', text='no'), NOT(Answer(ident='has_symptom_thick_patches')), salience=73)
    def ask_c2_6(self): self.declare(
        NextQuestion(ident='has_symptom_thick_patches'))
    cls.ask_c2_6 = ask_c2_6

    @Rule(Answer(ident='has_symptom_rash', text='yes'), Answer(ident='has_symptom_itching', text='yes'), Answer(ident='has_symptom_worse_at_night', text='no'), Answer(ident='has_symptom_dryness', text='no'), Answer(ident='has_symptom_ring_shaped_rash', text='no'), Answer(ident='has_symptom_white_patches', text='no'), Answer(ident='has_symptom_blisters', text='no'), Answer(ident='has_symptom_thick_patches', text='no'), NOT(Answer(ident='has_symptom_pimples')), salience=72)
    def ask_c2_7(self): self.declare(NextQuestion(ident='has_symptom_pimples'))
    cls.ask_c2_7 = ask_c2_7

    # --- Sub-Branch C.3: Non-Itchy Rashes ---
    @Rule(Answer(ident='has_symptom_rash', text='yes'), Answer(ident='has_symptom_itching', text='no'), NOT(Answer(ident='has_symptom_unilateral_rash')), salience=70)
    def ask_c3_1(self): self.declare(
        NextQuestion(ident='has_symptom_unilateral_rash'))
    cls.ask_c3_1 = ask_c3_1

    @Rule(Answer(ident='has_symptom_unilateral_rash', text='yes'), NOT(Answer(ident='has_symptom_pain')), salience=69)
    def ask_c3_1_pain(self): self.declare(
        NextQuestion(ident='has_symptom_pain'))
    cls.ask_c3_1_pain = ask_c3_1_pain

    @Rule(Answer(ident='has_symptom_rash', text='yes'), Answer(ident='has_symptom_itching', text='no'), Answer(ident='has_symptom_unilateral_rash', text='no'), NOT(Answer(ident='has_symptom_bulls_eye_rash')), salience=68)
    def ask_c3_2(self): self.declare(
        NextQuestion(ident='has_symptom_bulls_eye_rash'))
    cls.ask_c3_2 = ask_c3_2

    @Rule(Answer(ident='has_symptom_rash', text='yes'), Answer(ident='has_symptom_itching', text='no'), Answer(ident='has_symptom_unilateral_rash', text='no'), Answer(ident='has_symptom_bulls_eye_rash', text='no'), NOT(Answer(ident='has_symptom_butterfly_rash')), salience=67)
    def ask_c3_3(self): self.declare(
        NextQuestion(ident='has_symptom_butterfly_rash'))
    cls.ask_c3_3 = ask_c3_3

    @Rule(Answer(ident='has_symptom_rash', text='yes'), Answer(ident='has_symptom_itching', text='no'), Answer(ident='has_symptom_unilateral_rash', text='no'), Answer(ident='has_symptom_bulls_eye_rash', text='no'), Answer(ident='has_symptom_butterfly_rash', text='no'), NOT(Answer(ident='has_symptom_painful_blisters')), salience=66)
    def ask_c3_4(self): self.declare(
        NextQuestion(ident='has_symptom_painful_blisters'))
    cls.ask_c3_4 = ask_c3_4

    @Rule(Answer(ident='has_symptom_rash', text='yes'), Answer(ident='has_symptom_itching', text='no'), Answer(ident='has_symptom_unilateral_rash', text='no'), Answer(ident='has_symptom_bulls_eye_rash', text='no'), Answer(ident='has_symptom_butterfly_rash', text='no'), Answer(ident='has_symptom_painful_blisters', text='no'), NOT(Answer(ident='has_symptom_honey_colored_crusts')), salience=65)
    def ask_c3_5(self): self.declare(NextQuestion(
        ident='has_symptom_honey_colored_crusts'))
    cls.ask_c3_5 = ask_c3_5

    @Rule(Answer(ident='has_symptom_rash', text='yes'), Answer(ident='has_symptom_itching', text='no'), Answer(ident='has_symptom_unilateral_rash', text='no'), Answer(ident='has_symptom_bulls_eye_rash', text='no'), Answer(ident='has_symptom_butterfly_rash', text='no'), Answer(ident='has_symptom_painful_blisters', text='no'), Answer(ident='has_symptom_honey_colored_crusts', text='no'), NOT(Answer(ident='has_symptom_spreading_redness')), salience=64)
    def ask_c3_6(self): self.declare(
        NextQuestion(ident='has_symptom_spreading_redness'))
    cls.ask_c3_6 = ask_c3_6

    @Rule(Answer(ident='has_symptom_spreading_redness', text='yes'), NOT(Answer(ident='has_symptom_warmth')), salience=63)
    def ask_c3_6_warmth(self): self.declare(
        NextQuestion(ident='has_symptom_warmth'))
    cls.ask_c3_6_warmth = ask_c3_6_warmth

    @Rule(Answer(ident='has_symptom_rash', text='yes'), Answer(ident='has_symptom_itching', text='no'), Answer(ident='has_symptom_unilateral_rash', text='no'), Answer(ident='has_symptom_bulls_eye_rash', text='no'), Answer(ident='has_symptom_butterfly_rash', text='no'), Answer(ident='has_symptom_painful_blisters', text='no'), Answer(ident='has_symptom_honey_colored_crusts', text='no'), Answer(ident='has_symptom_spreading_redness', text='no'), NOT(Answer(ident='has_symptom_symmetrical_red_rash')), salience=62)
    def ask_c3_7(self): self.declare(NextQuestion(
        ident='has_symptom_symmetrical_red_rash'))
    cls.ask_c3_7 = ask_c3_7

    @Rule(Answer(ident='has_symptom_symmetrical_red_rash', text='yes'), NOT(Answer(ident='trigger_medications')), salience=61)
    def ask_c3_7_trigger(self): self.declare(
        NextQuestion(ident='trigger_medications'))
    cls.ask_c3_7_trigger = ask_c3_7_trigger

    # --- Branch D: Other conditions ---
    @Rule(Answer(ident='has_symptom_palpable_purpura', text='no'), NOT(Answer(ident='has_symptom_loss_of_pigment')), salience=50)
    def ask_d2(self): self.declare(
        NextQuestion(ident='has_symptom_loss_of_pigment'))
    cls.ask_d2 = ask_d2

    @Rule(Answer(ident='has_symptom_palpable_purpura', text='no'), Answer(ident='has_symptom_loss_of_pigment', text='no'), NOT(Answer(ident='has_symptom_brown_or_gray_patches')), salience=49)
    def ask_d3(self): self.declare(NextQuestion(
        ident='has_symptom_brown_or_gray_patches'))
    cls.ask_d3 = ask_d3

    @Rule(Answer(ident='has_symptom_palpable_purpura', text='no'), Answer(ident='has_symptom_loss_of_pigment', text='no'), Answer(ident='has_symptom_brown_or_gray_patches', text='no'), NOT(Answer(ident='has_symptom_discolored_patches')), salience=48)
    def ask_d4(self): self.declare(NextQuestion(
        ident='has_symptom_discolored_patches'))
    cls.ask_d4 = ask_d4

    @Rule(Answer(ident='has_symptom_palpable_purpura', text='no'), Answer(ident='has_symptom_loss_of_pigment', text='no'), Answer(ident='has_symptom_brown_or_gray_patches', text='no'), Answer(ident='has_symptom_discolored_patches', text='no'), NOT(Answer(ident='has_symptom_central_dimple')), salience=47)
    def ask_d5(self): self.declare(
        NextQuestion(ident='has_symptom_central_dimple'))
    cls.ask_d5 = ask_d5

    @Rule(Answer(ident='has_symptom_palpable_purpura', text='no'), Answer(ident='has_symptom_loss_of_pigment', text='no'), Answer(ident='has_symptom_brown_or_gray_patches', text='no'), Answer(ident='has_symptom_discolored_patches', text='no'), Answer(ident='has_symptom_central_dimple', text='no'), NOT(Answer(ident='has_symptom_rough_scaly_patch')), salience=46)
    def ask_d6(self): self.declare(NextQuestion(
        ident='has_symptom_rough_scaly_patch'))
    cls.ask_d6 = ask_d6

    @Rule(Answer(ident='has_symptom_palpable_purpura', text='no'), Answer(ident='has_symptom_loss_of_pigment', text='no'), Answer(ident='has_symptom_brown_or_gray_patches', text='no'), Answer(ident='has_symptom_discolored_patches', text='no'), Answer(ident='has_symptom_central_dimple', text='no'), Answer(ident='has_symptom_rough_scaly_patch', text='no'), NOT(Answer(ident='has_symptom_persistent_redness')), salience=45)
    def ask_d7(self): self.declare(NextQuestion(
        ident='has_symptom_persistent_redness'))
    cls.ask_d7 = ask_d7

    return cls
