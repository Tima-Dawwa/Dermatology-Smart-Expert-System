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

<<<<<<< Updated upstream
fungal_mcq_questions = [
    question(ident="fungal_locations", text="Where is the condition located?",
             valid=["scalp", "feet", "groin", "body", "mouth", "skin folds", "vagina", "trunk", "shoulders", "upper arms", "toenails", "fingernails"], Type="multi"),
]

# 2. Benign Growths Branch (Seborrheic Keratoses, Lipoma, Dermatofibroma, Warts, Molluscum Contagiosum)
benign_yes_no_questions = [
    ("waxy_appearance", "Do you have waxy appearance?"),
    ("color_change_brown_black", "Do you have color change (brown/black)?"),
    ("rough_texture", "Do you have rough texture?"),
    ("soft_lump_under_skin", "Do you have soft lump under skin?"),
    ("slow_growth", "Do you have slow growth?"),
    ("non_painful", "Is it non-painful?"),
    ("firm_nodule", "Do you have firm nodule?"),
    ("pigmentation", "Do you have pigmentation?"),
    ("dimpling_when_pinched", "Do you have dimpling when pinched?"),
    ("rough_raised_bumps", "Do you have rough raised bumps?"),
    ("flesh_colored_or_darker", "Is it flesh-colored or darker?"),
    ("pain_on_pressure", "Do you have pain on pressure (plantar)?"),
    ("pearly_dome_shaped_bumps", "Do you have pearly dome-shaped bumps?"),
    ("central_dimple", "Do you have central dimple?"),
    ("mild_itching_or_redness", "Do you have mild itching or redness?"),
    ("aging", "Are you experiencing aging-related changes?"),
    ("genetics", "Do you have genetic predisposition?"),
    ("minor_skin_injuries", "Have you had minor skin injuries?"),
    ("hpv_infection", "Have you had HPV infection?"),
    ("skin_trauma", "Have you had skin trauma?"),
    ("weakened_immunity", "Do you have weakened immunity?"),
    ("skin_to_skin_contact", "Have you had skin-to-skin contact?"),
    ("shared_towels", "Have you shared towels?"),
]

benign_mcq_questions = [
    question(ident="benign_locations", text="Where is the growth located?",
             valid=["chest", "back", "scalp", "face", "shoulders", "neck", "arms", "legs", "hands", "feet", "fingers", "knees", "trunk", "groin"], Type="multi"),
]

# 3. Viral Infections Branch (HSV, Herpes Zoster)
viral_yes_no_questions = [
    ("painful_blisters", "Do you have painful blisters?"),
    ("tingling_or_burning_before_rash",
     "Do you have tingling or burning before rash?"),
    ("crusting_sores", "Do you have crusting sores?"),
    ("painful_rash", "Do you have painful rash?"),
    ("blistering", "Do you have blistering?"),
    ("burning_or_tingling", "Do you have burning or tingling?"),
    ("sun_exposure", "Have you had sun exposure?"),
    ("previous_chickenpox_infection", "Have you had previous chickenpox infection?"),
    ("weakened_immunity", "Do you have weakened immunity?"),
    ("illness", "Have you been ill recently?"),
    ("viral_infection", "Have you had viral infection (HSV/HPV)?"),
    ("sexual_contact", "Have you had sexual contact?"),
]

viral_mcq_questions = [
    question(ident="viral_locations", text="Where is the condition located?",
             valid=["lips", "genitals", "buttocks", "torso", "face", "back", "genital area", "mouth"], Type="multi"),
]

# 4. Nail Disorders Branch (Paronychia, Nail Psoriasis, Beau's Lines, Koilonychia)
nail_yes_no_questions = [
    ("swelling_around_nail", "Do you have swelling around nail?"),
    ("redness_and_tenderness", "Do you have redness and tenderness?"),
    ("pus_formation", "Do you have pus formation?"),
    ("pitting", "Do you have pitting?"),
    ("nail_separation", "Do you have nail separation?"),
    ("discoloration_oil_spots", "Do you have discoloration (oil spots)?"),
    ("horizontal_nail_grooves", "Do you have horizontal nail grooves?"),
    ("nail_thinning", "Do you have nail thinning?"),
    ("concave_nail_shape", "Do you have concave nail shape?"),
    ("thin_brittle_nails", "Do you have thin, brittle nails?"),
    ("nail_biting", "Do you bite your nails?"),
    ("manicures", "Have you had manicures?"),
    ("moisture_exposure", "Have you had moisture exposure?"),
    ("psoriasis_flare_ups", "Have you had psoriasis flare-ups?"),
    ("severe_illness", "Have you had severe illness?"),
    ("chemotherapy", "Have you had chemotherapy?"),
    ("iron_deficiency", "Do you have iron deficiency?"),
    ("genetic_factors", "Do you have genetic factors?"),
]

nail_mcq_questions = [
    question(ident="nail_locations", text="Which nails are affected?",
             valid=["fingernails", "toenails"], Type="multi"),
]

# 5. Eczema/Atopic Dermatitis Branch
eczema_yes_no_questions = [
    ("dry_skin", "Do you have dry skin?"),
    ("redness_and_inflammation", "Do you have redness and inflammation?"),
    ("crusting_or_oozing", "Do you have crusting or oozing?"),
    ("weather_changes", "Have you experienced weather changes?"),
    ("irritants", "Have you been exposed to irritants (soaps, wool)?"),
]

eczema_mcq_questions = [
    question(ident="eczema_locations", text="Where is the eczema located?",
             valid=["face", "neck", "elbows", "knees", "hands", "arms"], Type="multi"),
]

# 6. Psoriasis Branch
psoriasis_yes_no_questions = [
    ("infections", "Have you had infections?"),
]

psoriasis_mcq_questions = [
    question(ident="psoriasis_locations", text="Where is the psoriasis located?",
             valid=["scalp", "elbows", "knees"], Type="multi"),
]

# 7. Acne/Rosacea Branch
acne_yes_no_questions = [
    ("pimples", "Do you have pimples?"),
    ("oiliness", "Do you have oiliness?"),
    ("hormones", "Are you experiencing hormonal changes?"),
    ("diet", "Have you had dietary changes?"),
]

acne_mcq_questions = [
    question(ident="acne_locations", text="Where is the acne/rosacea located?",
             valid=["face", "back", "chest"], Type="multi"),
]

# 8. Hair Loss Branch
hair_loss_yes_no_questions = [
    ("hair_thinning", "Do you have hair thinning?"),
    ("patchy_baldness", "Do you have patchy baldness?"),
    ("hair_shedding", "Do you have hair shedding?"),
    ("autoimmune_disorders", "Do you have autoimmune disorders?"),
]

hair_loss_mcq_questions = [
    question(ident="hair_loss_locations", text="Where is the hair loss?",
             valid=["scalp"], Type="multi"),
]

# 9. Contact Dermatitis Branch
contact_yes_no_questions = [
    ("rash", "Do you have rash?"),
    ("blisters", "Do you have blisters?"),
    ("plants", "Have you been exposed to plants (poison ivy/oak)?"),
    ("chemicals", "Have you been exposed to chemicals?"),
    ("fragrances", "Have you been exposed to fragrances?"),
]

contact_mcq_questions = [
    question(ident="contact_locations", text="Where is the contact dermatitis?",
             valid=["arms", "legs", "trunk", "face", "hands", "exposed skin areas"], Type="multi"),
]

# 10. Pigmentation Disorders Branch
pigmentation_yes_no_questions = [
    ("white_or_dark_patches", "Do you have white or dark patches?"),
    ("irregular_pigmentation", "Do you have irregular pigmentation?"),
    ("sun_exposure", "Have you had sun exposure?"),
    ("autoimmune_disorders", "Do you have autoimmune disorders?"),
]

pigmentation_mcq_questions = [
    question(ident="pigmentation_locations", text="Where are the pigmentation changes?",
             valid=["face", "neck", "hands"], Type="multi"),
]

# 11. Serious/Malignant Conditions Branch (Bullous Disease, Systemic Disease, Vasculitis, Malignant Skin Lesions)
malignant_yes_no_questions = [
    ("pain", "Do you have pain?"),
    ("joint_pain", "Do you have joint pain?"),
    ("ulcer", "Do you have ulcer?"),
    ("autoimmune_response", "Do you have autoimmune response?"),
    ("infections", "Have you had infections?"),
    ("uv_radiation", "Have you been exposed to UV radiation?"),
    ("aging", "Are you experiencing aging?"),
    ("genetics_malignant", "Do you have genetic predisposition?"),
    ("rash_location", "Do you have a rash in variable locations?"),
]

malignant_mcq_questions = [
    question(ident="malignant_locations", text="Where is the lesion/condition?",
             valid=["arms", "trunk", "legs", "face", "ears", "scalp", "hands", "genital area", "mouth", "buttocks", "chest", "feet", "fingers"], Type="multi"),
]

# 12. Cellulitis Impetigo and other Bacterial Infections
cellulitis_yes_no_questions = [
    ("redness", "Do you have redness on the affected area?"),
    ("pain", "Is the area painful?"),
    ("swelling", "Is the area swollen?"),
    ("warmth", "Does the area feel warm to the touch?"),
    ("fever", "Have you had a fever?"),
]

cellulitis_mcq_questions = [
    question(
        ident="cellulitis_locations",
        text="Where is the cellulitis located?",
        valid=["legs", "arms", "face"],
        Type="multi",
    ),
]

impetigo_yes_no_questions = [
    ("blisters", "Do you have blisters on your skin?"),
    ("crusting", "Do the blisters form a yellowish crust?"),
    ("itching", "Does the affected area itch?"),
    ("spread", "Is the rash spreading to other areas?"),
]

impetigo_mcq_questions = [
    question(
        ident="impetigo_locations",
        text="Where is the impetigo located?",
        valid=["face", "around mouth and nose", "arms"],
        Type="multi",
    ),
]

# 13. Lupus and other Connective Tissue diseases
lupus_yes_no_questions = [
    ("rash", "Do you have a skin rash?"),
    ("joint_pain", "Do you have joint pain?"),
    ("photosensitivity", "Does the rash worsen with sun exposure?"),
    ("fatigue", "Do you often feel unusually tired?"),
]

lupus_mcq_questions = [
    question(
        ident="lupus_locations",
        text="Where is the lupus rash located?",
        valid=["face (butterfly rash)", "arms", "chest"],
        Type="multi",
    ),
]

connective_tissue_yes_no_questions = [
    ("joint_pain", "Do you have joint pain?"),
    ("rash", "Do you have a rash on your skin?"),
    ("photosensitivity", "Does the rash worsen with sun exposure?"),
]

connective_tissue_mcq_questions = [
    question(
        ident="connective_tissue_locations",
        text="Where is the rash located?",
        valid=["face", "hands", "chest"],
        Type="multi",
    ),
]

# 14. Melanoma Skin Cancer Nevi and Moles
melanoma_yes_no_questions = [
    ("discoloration", "Do you notice any changes in skin color or a new dark spot?"),
    ("ulcer", "Do you have a non-healing ulcer or sore?"),
    ("bleeding", "Is the lesion bleeding spontaneously?"),
    ("enlarging_rapidly", "Has the lesion grown rapidly?"),
    ("mole_change", "Has an existing mole changed in size, shape, or color?"),
]

melanoma_mcq_questions = [
    question(
        ident="melanoma_locations",
        text="Where is the suspicious lesion located?",
        valid=["back", "legs", "arms", "face"],
        Type="multi",
    ),
]

nevi_yes_no_questions = [
    (
        "discoloration",
        "Do you notice any changes in skin color or a new pigmented spot?",
    ),
    ("mole_change", "Has a mole changed in size, shape, or color?"),
    ("itching", "Does the mole itch?"),
    ("bleeding", "Does the mole bleed or crust?"),
]

nevi_mcq_questions = [
    question(
        ident="nevi_locations",
        text="Where is the mole or pigmented spot located?",
        valid=["any skin area"],
        Type="multi",
    ),
]

# 15. Scabies Lyme Disease and other Infestations and Bites
scabies_yes_no_questions = [
    ("itching", "Is the itching worse at night?"),
    ("rash_between_fingers", "Is the rash located between your fingers?"),
    (
        "contact_history",
        "Have you been in close contact with someone with similar symptoms?",
    ),
]

scabies_mcq_questions = [
    question(
        ident="scabies_locations",
        text="Where is the rash located?",
        valid=["between fingers", "wrists", "waist", "armpits"],
        Type="multi",
    ),
]

lyme_disease_yes_no_questions = [
    ("rash", "Do you have a rash?"),
    ("joint_pain", "Do you have joint pain?"),
    ("fatigue", "Do you feel unusually tired?"),
    ("tick_bite", "Have you had a recent tick bite?"),
]

lyme_disease_mcq_questions = [
    question(
        ident="lyme_disease_locations",
        text="Where is the rash located?",
        valid=["arms", "legs", "torso"],
        Type="multi",
    ),
]

# ADDITIONAL QUESTIONS FOR EXANTHEMS AND DRUG ERUPTIONS:

# Missing symptoms that need questions:
additional_yes_no_questions = [
    # From Exanthems and Drug Eruptions (not covered in other branches)
    ("viral_infections_trigger", "Have you had viral infections recently?"),
    ("medications_trigger", "Have you started any new medications?"),
]

# Combine all binary questions by branch
all_binary_questions = (
    general_yes_no_questions +
    fungal_yes_no_questions +
    benign_yes_no_questions +
    viral_yes_no_questions +
    nail_yes_no_questions +
    eczema_yes_no_questions +
    psoriasis_yes_no_questions +
    acne_yes_no_questions +
    hair_loss_yes_no_questions +
    contact_yes_no_questions +
    pigmentation_yes_no_questions +
    malignant_yes_no_questions +
    cellulitis_yes_no_questions+
    impetigo_yes_no_questions+
    lupus_yes_no_questions+
    connective_tissue_yes_no_questions+
    melanoma_yes_no_questions+
    nevi_yes_no_questions+
    scabies_yes_no_questions+
    lyme_disease_yes_no_questions+
    additional_yes_no_questions 
=======
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
>>>>>>> Stashed changes
)

# Helper to get questions data fast
question_lookup = {q['ident']: q for q in questions_list}

<<<<<<< Updated upstream
# Combine all MCQ questions
all_mcq_questions = (
    general_mcq_questions
    + fungal_mcq_questions
    + benign_mcq_questions
    + viral_mcq_questions
    + nail_mcq_questions
    + eczema_mcq_questions
    + psoriasis_mcq_questions
    + acne_mcq_questions
    + hair_loss_mcq_questions
    + contact_mcq_questions
    + pigmentation_mcq_questions
    + malignant_mcq_questions
    + cellulitis_mcq_questions
    + impetigo_mcq_questions
    + lupus_mcq_questions
    + connective_tissue_mcq_questions
    + melanoma_mcq_questions
    + nevi_mcq_questions
    + scabies_mcq_questions
    + lyme_disease_mcq_questions
)
=======
>>>>>>> Stashed changes

def get_question_by_ident(ident):
    return question_lookup.get(ident)
