from ExpertSystem.facts import question

# Text-input questions
text_questions = [
    question(ident="age", text="What is your age?", valid=[], Type="text"),
    question(ident="symptom_duration",
             text="How long have the symptoms lasted?", valid=[], Type="text"),
    question(ident="rash_location", text="Where is the rash located?",
             valid=[], Type="text"),
]

# Binary (yes/no) questions
yes_no_questions = [
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
    ("trigger_cosmetics", "Did the symptoms appear after using a cosmetic or cream?"),
    ("joint_pain", "Do you have joint pain along with the rash?"),
    ("rash_between_fingers", "Is the rash between your fingers?"),
    ("rash_scalp", "Do you have flaking or redness on your scalp?"),
    ("bleeding", "Is the lesion bleeding spontaneously?"),
    ("enlarging_rapidly", "Has the lesion grown rapidly in size?"),
    ("crusting_scalp", "Is there crusting or scaling on your scalp?"),
    ("mucosal_involvement", "Are your lips, mouth or genitals also affected?"),
    ("sun_exposure_area", "Is the lesion in a sun-exposed area?"),
    ("history_cancer", "Do you have a personal or family history of cancer?"),
    ("recurrence", "Has the rash appeared in the same area before?"),
    ("drug_history", "Did you recently start any new medications?"),
    ("rash_symmetry", "Is the rash symmetrical on both sides of the body?"),
    ("vesicles", "Do you have small fluid-filled blisters or vesicles?"),
    ("itching_exanthems", "Do you experience itching in the affected area?"),
    ("hair_loss_alopecia", "Are you experiencing hair loss or thinning?"),
    ("acne", "Do you have pimples, blackheads, or whiteheads on your face or back?"),
    ("rosacea", "Do you experience facial redness, especially on your cheeks and nose?"),
    ("contact_history", "Have you been in contact with plants or chemicals that might cause a reaction?"),
    ("skin_lightening", "Have you noticed any areas of skin becoming lighter or darker?"),
    ("sun_sensitivity_light_disorders",
     "Does the condition worsen after sun exposure?"),
]

binary_questions = [
    question(ident=ident, text=text, valid=["yes", "no"], Type="multi")
    for ident, text in yes_no_questions
]

basic_questions = text_questions + binary_questions
