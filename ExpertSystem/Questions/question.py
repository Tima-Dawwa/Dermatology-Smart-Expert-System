from ExpertSystem.facts import question

ALL_SYMPTOMS = sorted(list(set([
    'asymmetry', 'black_dots', 'blackheads', 'bleeding', 'blisters', 'border_irregularity',
    'brown_or_gray_patches', 'bulls_eye_rash', 'bumps', 'burning', 'butterfly_rash',
    'central_dimple', 'color_variation', 'cracking_skin', 'crusting', 'cysts',
    'debris_under_nail', 'diameter_greater_than_6mm', 'dimpling', 'dimpling_when_squeezed',
    'discoid_lesions', 'discoloration', 'discolored_patches', 'dryness', 'evolution',
    'evolution_of_mole', 'fatigue', 'fever', 'firm_lump', 'flesh_colored', 'flushing',
    'hair_shedding', 'hair_thinning', 'honey_colored_crusts', 'intense_itching',
    'irregular_pigmentation', 'itching', 'joint_pain', 'large_tense_blisters', 'loss_of_pigment',
    'lump_or_growth', 'macules_and_papules', 'movable_under_skin', 'nail_brittleness',
    'nail_concavity', 'nail_fold_swelling', 'nail_grooves', 'nail_pitting', 'nail_separation',
    'nail_thickening', 'nail_thinning', 'oil_drop_stain', 'oozing', 'oozing_or_crusting',
    'pain', 'painful_blisters', 'palpable_purpura', 'patchy_baldness', 'patchy_hair_loss',
    'pearl_like_appearance', 'pearly_bump', 'persistent_redness', 'persistent_scaly_patch',
    'photosensitivity', 'pimples', 'pink_or_red_spot', 'pus', 'raised_edges',
    'raised_lesion_with_central_depression', 'rash', 'rash_with_burrows', 'red_or_purple_spots',
    'red_sores', 'red_urticarial_plaques', 'redness', 'ring_shaped_rash', 'rough_bumps',
    'rough_scaly_patch', 'sandpaper_feel', 'scaling', 'severe_itching', 'severe_pain',
    'slow_growth', 'small_bumps', 'smooth_bald_patches', 'soft_lump', 'sore_that_wont_heal',
    'spreading_redness', 'stuck_on_look', 'sudden_onset', 'swelling', 'symmetrical_facial_patches',
    'symmetrical_patches', 'symmetrical_red_rash', 'thick_patches', 'thin_nails', 'tingling',
    'ulcers', 'unilateral_rash', 'visible_blood_vessels', 'warmth', 'wart_like_growth',
    'waxy_appearance', 'white_patches', 'white_patches_of_skin', 'whiteheads', 'worse_at_night',
    "transverse_nail_grooves"
])))

# This list contains every unique trigger gathered from the disease information.
ALL_TRIGGERS = sorted(list(set([
    'actinic_keratosis', 'age', 'aging', 'alcohol', 'allergens', 'antibiotics',
    'autoimmune', 'autoimmune_reaction', 'bacteria', 'birth_control_pills',
    'chemicals', 'chemotherapy', 'close_contact', 'chronic_sun_exposure', 'diabetes',
    'dry_weather', 'fragrances', 'genetics', 'genetic_factors', 'high_fever',
    'hormonal_changes', 'hormones', 'hot_drinks', 'hpv_infection', 'humidity',
    'illness', 'immunosuppression', 'infestation_by_mite', 'infections', 'injury',
    'insect_bites', 'iron_deficiency_anemia', 'long_term_sun_exposure', 'manicures',
    'medications', 'metals', 'minor_injuries', 'moisture', 'multiple_atypical_moles',
    'nail_biting', 'nickel', 'nsaids', 'oily_skin', 'plants', 'poison_ivy',
    'poxvirus_infection', 'pregnancy', 'psoriasis_flares', 'public_showers',
    'reactivation_of_chickenpox_virus', 'severe_illness', 'shared_items', 'skin_break',
    'skin_contact', 'skin_injury', 'skin_trauma', 'spicy_food', 'stress', 'sun_exposure',
    'sweating', 'sweaty_feet', 'tick_bite', 'tight_shoes', 'trauma', 'uv_radiation',
    'viral_infection', 'warm_moist_environments', 'weakened_immunity'
])))


# --- Comprehensive List of All Questions ---
questions_list = [
    # --- Demographic and Foundational Questions ---
    question(
        ident='age',
        text='What is your age?',
        Type='number',
        valid=[]
    ),
    question(
        ident='duration',
        text='How long have you had these symptoms?',
        Type='multi',
        valid=[
            "1-2 weeks", "1-3 weeks", "2-4 weeks", "weeks to months",
            "months to years", "chronic", "chronic with flares"
        ]
    ),
    question(
        ident='severity',
        text='How Severe is the disease?',
        Type='multi',
        valid=["mild", "moderate", "severe"]
    ),
    question(
        ident='locations',
        text='Where on your body are the symptoms located? (Select all that apply)',
        Type='multi',
        valid=sorted(list(set([
            'arms', 'face', 'neck', 'elbows', 'knees', 'scalp', 'lower_back', 'exposed_areas',
            'back', 'chest', 'shoulders', 'body', 'legs', 'feet', 'between_toes', 'mouth',
            'groin', 'skin_folds', 'vagina', 'trunk', 'upper_arms', 'hands',
            'fingers', 'lips', 'genitals', 'buttocks', 'torso', 'fingernails', 'toenails',
            'any_skin_area', 'beard', 'eyebrows', 'armpits', 'cheeks', 'nose', 'forehead',
            'ears', 'wrists', 'waist'
        ])))
    ),
]

# --- Dynamically Generated Yes/No Question for Every Symptom ---
for symptom in ALL_SYMPTOMS:
    # Create a user-friendly version of the symptom for the question text
    symptom_text = symptom.replace('_', ' ')

    questions_list.append(
        question(
            ident=f'has_symptom_{symptom}',
            text=f'Are you experiencing: {symptom_text}?',
            Type='multi',
            valid=['yes', 'no']
        )
    )

# --- Concluding Multi-Select Question for Triggers ---
questions_list.append(
    question(
        ident='triggers',
        text='Have you noticed any of the following triggers making your condition worse? (Select all that apply)',
        Type='multi',
        valid=ALL_TRIGGERS
    ),
)
questions_list.append(
    question(ident='affects_nails_or_hair',
             text="Are your symptoms primarily affecting your nails or hair?", valid=['yes', 'no']),
)
questions_list.append(
    question(ident='trigger_contact_related',
             text="Did the rash appear after coming into contact with a new substance, like a plant, metal, or lotion?", valid=['yes', 'no']),
)
questions_list.append(
    question(ident='trigger_medications',
             text="Did the rash appear after starting a new medication?", valid=['yes', 'no']),
)

# Helper to get questions data fast
question_lookup = {q['ident']: q for q in questions_list}


def get_question_by_ident(ident):
    return question_lookup.get(ident)
