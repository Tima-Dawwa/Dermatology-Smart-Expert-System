from ExpertSystem.facts import question
from ExpertSystem.Data import disease

# General questions (applicable to all branches)
general_mcq_questions = [
    question(ident="age_range", text="What is your age?",
             valid=[], Type="number"),

    question(ident="severity_levels", text="How would you rate the severity?",
             valid=["mild", "moderate", "severe"], Type="multi"),

    question(ident="common_duration", text="How long have you had this condition?",
             valid=disease.DURATION_OPTIONS, Type="multi"),
]

# General binary questions
general_yes_no_questions = [
    ("itching", "Do you have itching?"),
    ("redness", "Do you have redness?"),
    ("dryness", "Do you have dryness?"),
    ("scaling", "Do you have scaling?"),
    ("stress", "Have you been under stress?"),
    ("allergens", "Have you been exposed to allergens?"),
]

# 1. Fungal Infections Branch (Tinea, Candidiasis, Tinea Versicolor, Onychomycosis)
fungal_yes_no_questions = [
    ("ring_shaped_rash", "Do you have ring-shaped rash?"),
    ("scaly_skin", "Do you have scaly skin?"),
    ("red_rash", "Do you have red rash?"),
    ("white_patches_oral_vaginal", "Do you have white patches (oral/vaginal)?"),
    ("itching_or_burning", "Do you have itching or burning?"),
    ("discolored_patches", "Do you have discolored patches?"),
    ("mild_scaling", "Do you have mild scaling?"),
    ("slight_itching", "Do you have slight itching?"),
    ("thickened_nails", "Do you have thickened nails?"),
    ("discoloration", "Do you have discoloration?"),
    ("brittle_or_crumbly_nails", "Do you have brittle or crumbly nails?"),
    ("warm_moist_environments", "Have you been in warm, moist environments?"),
    ("skin_contact", "Have you had skin contact with affected person?"),
    ("shared_items", "Have you shared items with others?"),
    ("antibiotics", "Have you taken antibiotics?"),
    ("diabetes", "Do you have diabetes?"),
    ("immunosuppression", "Are you immunosuppressed?"),
    ("moisture", "Have you been exposed to moisture?"),
    ("humidity", "Have you been in humid conditions?"),
    ("oily_skin", "Do you have oily skin?"),
    ("tight_shoes", "Do you wear tight shoes?"),
    ("trauma", "Have you had trauma to the area?"),
]

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
    additional_yes_no_questions
)

binary_questions = [
    question(ident=ident, text=text, valid=["yes", "no"], Type="multi")
    for ident, text in all_binary_questions
]

# Combine all MCQ questions
all_mcq_questions = (
    general_mcq_questions +
    fungal_mcq_questions +
    benign_mcq_questions +
    viral_mcq_questions +
    nail_mcq_questions +
    eczema_mcq_questions +
    psoriasis_mcq_questions +
    acne_mcq_questions +
    hair_loss_mcq_questions +
    contact_mcq_questions +
    pigmentation_mcq_questions +
    malignant_mcq_questions
)

# Final combined questions list
basic_questions = binary_questions + all_mcq_questions
