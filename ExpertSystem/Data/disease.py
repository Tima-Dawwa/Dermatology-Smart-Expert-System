from ExpertSystem.facts import DiseaseInfo

diseases = [
    DiseaseInfo(
        name="Eczema (Atopic Dermatitis)",
        common_symptoms={
            "itching": "high",
            "dryness": "high",
            "redness": "medium",
            "scaling": "medium",
        },
        age_min=1,
        age_max=40,
        common_locations=["arms", "face", "neck", "elbows", "knees"],
        severity_levels=["mild", "moderate", "severe"],
        common_duration="chronic with flares",
        triggers=["stress", "allergens", "dry_weather"],
        common_treatments=["moisturizers", "topical corticosteroids", "antihistamines"],
        notes="Often associated with asthma and allergic rhinitis. Flares up in dry or cold weather.",
    ),
    DiseaseInfo(
        name="Psoriasis",
        common_symptoms={
            "scaling": "high",
            "redness": "high",
            "thick_patches": "high",
            "itching": "medium",
        },
        age_min=20,
        age_max=60,
        common_locations=["scalp", "elbows", "knees", "lower_back"],
        severity_levels=["mild", "moderate", "severe"],
        common_duration="chronic",
        triggers=["stress", "infections", "skin_injury"],
        common_treatments=["coal tar", "topical steroids", "phototherapy"],
        notes="A chronic autoimmune condition characterized by well-demarcated, silvery-white scales.",
    ),
    DiseaseInfo(
        name="Contact Dermatitis",
        common_symptoms={
            "itching": "high",
            "redness": "high",
            "blisters": "medium",
            "burning": "medium",
        },
        age_min=0,
        age_max=100,
        common_locations=["exposed_areas"],
        severity_levels=["mild", "moderate", "severe"],
        common_duration="1-3 weeks",
        triggers=["plants (poison_ivy)", "chemicals", "metals (nickel)", "fragrances"],
        common_treatments=[
            "topical corticosteroids",
            "oral antihistamines",
            "cool compresses",
        ],
        notes="Results from direct skin contact with an allergen or irritant; rash is confined to the area of exposure.",
    ),
    DiseaseInfo(
        name="Acne Vulgaris",
        common_symptoms={
            "pimples": "high",
            "blackheads": "high",
            "itching": "high",
            "whiteheads": "high",
            "cysts": "medium",
        },
        age_min=12,
        age_max=30,
        common_locations=["face", "back", "chest", "shoulders"],
        severity_levels=["mild", "moderate", "severe"],
        common_duration="months to years",
        triggers=["hormones", "stress", "oily_skin", "bacteria"],
        common_treatments=["topical retinoids", "benzoyl peroxide", "oral antibiotics"],
        notes="Very common in teenagers and young adults due to hormonal changes.",
    ),
    DiseaseInfo(
        name="Rosacea",
        common_symptoms={
            "persistent_redness": "high",
            "flushing": "high",
            "pimples": "medium",
            "visible_blood_vessels": "medium",
        },
        age_min=30,
        age_max=60,
        common_locations=["face (cheeks, nose, forehead)"],
        severity_levels=["mild", "moderate", "severe"],
        common_duration="chronic with flares",
        triggers=["sun_exposure", "hot_drinks", "spicy_food", "alcohol", "stress"],
        common_treatments=["topical metronidazole", "oral antibiotics", "sunscreen"],
        notes="More common in adults with fair skin. Often mistaken for acne.",
    ),
    DiseaseInfo(
        name="Tinea Corporis (Ringworm of the Body)",
        common_symptoms={
            "ring_shaped_rash": "high",
            "itching": "high",
            "scaling": "medium",
            "raised_edges": "high",
        },
        age_min=5,
        age_max=60,
        common_locations=["body", "arms", "legs"],
        severity_levels=["mild", "moderate"],
        common_duration="2-4 weeks",
        triggers=["warm_moist_environments", "skin_contact", "shared_items"],
        common_treatments=["topical antifungals", "oral antifungals"],
        notes="Highly contagious fungal infection. The name 'ringworm' is a misnomer; no worm is involved.",
    ),
    DiseaseInfo(
        name="Tinea Pedis (Athlete's Foot)",
        common_symptoms={
            "itching": "high",
            "scaling": "high",
            "cracking_skin": "medium",
            "blisters": "low",
        },
        age_min=10,
        age_max=50,
        common_locations=["feet (between_toes)"],
        severity_levels=["mild", "moderate"],
        common_duration="weeks to months",
        triggers=["sweaty_feet", "tight_shoes", "public_showers"],
        common_treatments=["antifungal creams", "powders", "keeping feet dry"],
        notes="A very common type of tinea infection.",
    ),
    DiseaseInfo(
        name="Candidiasis (Yeast Infection)",
        common_symptoms={
            "redness": "high",
            "itching": "high",
            "white_patches": "medium",
            "burning": "medium",
        },
        age_min=0,
        age_max=100,
        common_locations=["mouth (thrush)", "groin", "skin_folds", "vagina"],
        severity_levels=["mild", "moderate", "severe"],
        common_duration="1-2 weeks",
        triggers=["antibiotics", "diabetes", "immunosuppression", "moisture"],
        common_treatments=[
            "antifungal creams",
            "oral antifungals",
            "hygiene improvements",
        ],
        notes="Caused by an overgrowth of Candida yeast, especially Candida albicans.",
    ),
    DiseaseInfo(
        name="Tinea Versicolor",
        common_symptoms={"discolored_patches": "high", "scaling": "medium"},
        age_min=10,
        age_max=40,
        common_locations=["trunk", "shoulders", "upper_arms"],
        severity_levels=["mild"],
        common_duration="weeks to months",
        triggers=["humidity", "oily_skin", "sweating"],
        common_treatments=["antifungal shampoos", "topical antifungals"],
        notes="Caused by an overgrowth of yeast (Malassezia). Patches are often more visible after sun exposure.",
    ),
    DiseaseInfo(
        name="Warts (Verruca Vulgaris)",
        common_symptoms={
            "rough_bumps": "high",
            "black_dots": "medium",
            "flesh_colored": "high",
        },
        age_min=5,
        age_max=30,
        common_locations=["hands", "feet (plantar_warts)", "fingers", "knees"],
        severity_levels=["mild", "moderate"],
        common_duration="months to years",
        triggers=["hpv_infection", "skin_trauma", "weakened_immunity"],
        common_treatments=["cryotherapy", "salicylic acid", "laser therapy"],
        notes="Caused by Human Papillomavirus (HPV); can spread through contact.",
    ),
    DiseaseInfo(
        name="Molluscum Contagiosum",
        common_symptoms={"central_dimple": "high", "pearl_like_appearance": "medium"},
        age_min=1,
        age_max=10,
        common_locations=["trunk", "arms", "groin", "face"],
        severity_levels=["mild"],
        common_duration="6-12 months",
        triggers=["poxvirus_infection", "skin_contact", "shared_items"],
        common_treatments=["cryotherapy", "curettage", "topical agents"],
        notes="Common viral infection in children; often resolves on its own without treatment.",
    ),
    DiseaseInfo(
        name="Herpes Simplex Virus (HSV)",
        common_symptoms={
            "painful_blisters": "high",
            "tingling": "medium",
            "burning": "medium",
            "crusting": "high",
        },
        age_min=15,
        age_max=50,
        common_locations=["lips (cold_sores)", "genitals", "buttocks"],
        severity_levels=["mild", "moderate", "severe"],
        common_duration="1-2 weeks",
        triggers=["stress", "illness", "sun_exposure", "viral_infection"],
        common_treatments=["antivirals (acyclovir, valacyclovir)"],
        notes="Recurrent viral infection; HSV-1 is typically oral, while HSV-2 is typically genital, but crossover can occur.",
    ),
    DiseaseInfo(
        name="Herpes Zoster (Shingles)",
        common_symptoms={
            "unilateral_rash": "high",
            "severe_pain": "high",
            "blisters": "high",
            "burning": "high",
        },
        age_min=50,
        age_max=100,
        common_locations=["torso (dermatomal)", "face", "back"],
        severity_levels=["moderate", "severe"],
        common_duration="2-4 weeks",
        triggers=["reactivation_of_chickenpox_virus", "weakened_immunity", "age"],
        common_treatments=["antivirals", "pain relievers"],
        notes="Caused by reactivation of the varicella-zoster virus. A complication can be postherpetic neuralgia (lingering pain).",
    ),
    DiseaseInfo(
        name="Impetigo",
        common_symptoms={
            "honey_colored_crusts": "high",
            "blisters": "high",
            "red_sores": "high",
        },
        age_min=2,
        age_max=6,
        common_locations=["face (around_mouth_and_nose)", "arms", "legs"],
        severity_levels=["mild", "moderate"],
        common_duration="1-2 weeks",
        triggers=["bacterial_infection (staph, strep)"],
        common_treatments=["topical antibiotics", "oral antibiotics"],
        notes="Highly contagious bacterial skin infection, especially common in young children.",
    ),
    DiseaseInfo(
        name="Cellulitis",
        common_symptoms={
            "spreading_redness": "high",
            "pain": "high",
            "swelling": "high",
            "warmth": "high",
            "fever": "medium",
        },
        age_min=0,
        age_max=100,
        common_locations=["legs", "arms", "face"],
        severity_levels=["moderate", "severe"],
        common_duration="days to weeks",
        triggers=["bacterial_infection", "skin_break"],
        common_treatments=[
            "oral_or_intravenous_antibiotics",
            "elevation_of_affected_area",
        ],
        notes="A bacterial infection of the deeper layers of skin. Requires prompt medical attention as it can spread rapidly.",
    ),
    DiseaseInfo(
        name="Paronychia",
        common_symptoms={
            "nail_fold_swelling": "high",
            "redness": "high",
            "pain": "high",
            "pus": "medium",
        },
        age_min=0,
        age_max=100,
        common_locations=["fingernails", "toenails"],
        severity_levels=["mild", "moderate"],
        common_duration="1-4 weeks",
        triggers=["nail_biting", "manicures", "moisture", "injury"],
        common_treatments=["warm soaks", "antibiotics", "drainage"],
        notes="Infection of the skin around a fingernail or toenail. Can be acute (bacterial) or chronic (fungal).",
    ),
    DiseaseInfo(
        name="Seborrheic Keratosis",
        common_symptoms={
            "waxy_appearance": "high",
            "stuck_on_look": "high",
            "discoloration": "medium",
            "scaling": "medium",
        },
        age_min=50,
        age_max=100,
        common_locations=["chest", "back", "scalp", "face"],
        severity_levels=["mild"],
        common_duration="chronic",
        triggers=["aging", "genetics", "sun_exposure"],
        common_treatments=["cryotherapy", "curettage"],
        notes="Benign, non-cancerous growth. Often mistaken for melanoma due to its dark, irregular appearance.",
    ),
    DiseaseInfo(
        name="Seborrheic Dermatitis",
        common_symptoms={
            "scaly_patch": "high",
            "itching": "high",
            "redness": "medium",
            "greasy_appearance": "medium",
        },
        age_min=0,
        age_max=100,
        common_locations=["scalp", "face", "ears", "chest", "upper back"],
        severity_levels=["mild", "moderate"],
        common_duration="chronic with flare-ups",
        triggers=["stress", "cold_weather", "hormonal_changes", "Malassezia yeast"],
        common_treatments=[
            "medicated_shampoos",
            "topical_steroids",
            "antifungal_creams",
        ],
        notes="A chronic inflammatory skin condition. Not contagious and not related to poor hygiene. Often confused with psoriasis or eczema.",
    ),
    DiseaseInfo(
        name="Lipoma",
        common_symptoms={
            "soft_lump": "high",
            "slow_growth": "high",
            "movable_under_skin": "high",
        },
        age_min=30,
        age_max=60,
        common_locations=["shoulders", "back", "neck", "arms"],
        severity_levels=["mild"],
        common_duration="chronic",
        triggers=["genetics"],
        common_treatments=["no_treatment_needed", "surgical_excision"],
        notes="Benign fatty tumor; usually painless unless it compresses a nerve.",
    ),
    DiseaseInfo(
        name="Dermatofibroma",
        common_symptoms={
            "firm_lump": "high",
            "dimpling_when_squeezed": "high",
            "discoloration": "medium",
        },
        age_min=20,
        age_max=50,
        common_locations=["legs", "arms"],
        severity_levels=["mild"],
        common_duration="chronic",
        triggers=["minor_injuries", "insect_bites"],
        common_treatments=["no_treatment_needed", "surgical_removal"],
        notes="Benign fibrous nodule in the skin. Often feels like a small, hard button under the skin.",
    ),
    DiseaseInfo(
        name="Alopecia Areata",
        common_symptoms={
            "patchy_hair_loss": "high",
            "smooth_bald_patches": "high",
            "sudden_onset": "medium",
        },
        age_min=20,
        age_max=40,
        common_locations=["scalp", "beard", "eyebrows"],
        severity_levels=["mild", "moderate", "severe"],
        common_duration="weeks to months",
        triggers=["autoimmune", "stress", "genetics"],
        common_treatments=["corticosteroids", "minoxidil", "immunotherapy"],
        notes="An autoimmune disorder that causes hair to fall out in small, round patches.",
    ),
    DiseaseInfo(
        name="Onychomycosis (Fungal Nails)",
        common_symptoms={
            "nail_thickening": "high",
            "discoloration": "high",
            "nail_brittleness": "medium",
            "debris_under_nail": "medium",
        },
        age_min=40,
        age_max=100,
        common_locations=["toenails", "fingernails"],
        severity_levels=["mild", "moderate", "severe"],
        common_duration="months to years",
        triggers=["tight_shoes", "moisture", "trauma", "aging"],
        common_treatments=["oral antifungals", "medicated nail lacquers"],
        notes="Fungal infection of the nail. Treatment is often long, and recurrence is common.",
    ),
    DiseaseInfo(
        name="Nail Psoriasis",
        common_symptoms={
            "nail_pitting": "high",
            "nail_separation": "medium",
            "discoloration": "medium",
            "oil_drop_stain": "medium",
        },
        age_min=20,
        age_max=60,
        common_locations=["fingernails", "toenails"],
        severity_levels=["mild", "moderate", "severe"],
        common_duration="chronic",
        triggers=["psoriasis_flares", "trauma"],
        common_treatments=["topical steroids", "systemic therapies"],
        notes="Occurs in up to 50% of people with psoriasis and can be a sign of psoriatic arthritis.",
    ),
    DiseaseInfo(
        name="Koilonychia (Spoon Nails)",
        common_symptoms={
            "nail_concavity": "high",
            "nail_brittleness": "medium",
            "thin_nails": "high",
        },
        age_min=0,
        age_max=100,
        common_locations=["fingernails"],
        severity_levels=["mild", "moderate"],
        common_duration="chronic unless treated",
        triggers=["iron_deficiency_anemia", "genetics", "trauma"],
        common_treatments=["iron supplementation", "addressing_underlying_cause"],
        notes="Often a sign of an underlying systemic issue, most commonly iron deficiency anemia.",
    ),
    DiseaseInfo(
        name="Beau's Lines",
        common_symptoms={"transverse_nail_grooves": "high", "nail_thinning": "low"},
        age_min=0,
        age_max=100,
        common_locations=["fingernails", "toenails"],
        severity_levels=["mild"],
        common_duration="1-3 months",
        triggers=["severe_illness", "high_fever", "trauma", "chemotherapy"],
        common_treatments=["treat_underlying_cause", "wait_for_nail_to_grow_out"],
        notes="Reflects a temporary interruption of nail growth due to a past systemic stressor.",
    ),
    DiseaseInfo(
        name="Vitiligo",
        common_symptoms={
            "white_patches_of_skin": "high",
            "loss_of_pigment": "high",
            "symmetrical_patches": "medium",
        },
        age_min=10,
        age_max=30,
        common_locations=["face", "hands", "armpits", "groin"],
        severity_levels=["mild", "moderate", "severe"],
        common_duration="chronic",
        triggers=["autoimmune", "genetics", "stress"],
        common_treatments=[
            "topical corticosteroids",
            "phototherapy",
            "cosmetic_cover_up",
        ],
        notes="Autoimmune condition where pigment-producing cells (melanocytes) are destroyed.",
    ),
    DiseaseInfo(
        name="Melasma",
        common_symptoms={
            "brown_or_gray_patches": "high",
            "symmetrical_facial_patches": "high",
        },
        age_min=20,
        age_max=50,
        common_locations=["face (cheeks, forehead, upper_lip)"],
        severity_levels=["mild", "moderate"],
        common_duration="months to years",
        triggers=[
            "sun_exposure",
            "hormonal_changes (pregnancy)",
            "birth_control_pills",
        ],
        common_treatments=["sunscreen", "hydroquinone", "tretinoin"],
        notes="Often called the 'mask of pregnancy.' Much more common in women.",
    ),
    DiseaseInfo(
        name="Lupus (Cutaneous)",
        common_symptoms={
            "butterfly_rash": "high",
            "photosensitivity": "high",
            "discoid_lesions": "medium",
            "joint_pain": "medium",
        },
        age_min=20,
        age_max=50,
        common_locations=["face", "scalp", "ears", "arms", "chest"],
        severity_levels=["mild", "moderate", "severe"],
        common_duration="chronic with flares",
        triggers=["autoimmune_reaction", "sun_exposure", "infections"],
        common_treatments=["corticosteroids", "immunosuppressants", "sun_protection"],
        notes="Autoimmune disease with systemic symptoms; skin rash often worsens with sun exposure.",
    ),
    DiseaseInfo(
        name="Vasculitis",
        common_symptoms={
            "palpable_purpura": "high",
            "ulcers": "medium",
            "pain": "medium",
            "red_or_purple_spots": "high",
        },
        age_min=30,
        age_max=70,
        common_locations=["legs", "feet", "buttocks"],
        severity_levels=["moderate", "severe"],
        common_duration="weeks to months",
        triggers=["autoimmune", "infections", "medications"],
        common_treatments=["corticosteroids", "immunosuppressants"],
        notes="Inflammation of blood vessels causing leakage and damage to the skin.",
    ),
    DiseaseInfo(
        name="Bullous Pemphigoid",
        common_symptoms={
            "large_tense_blisters": "high",
            "severe_itching": "high",
            "red_urticarial_plaques": "medium",
        },
        age_min=60,
        age_max=100,
        common_locations=["arms", "trunk", "legs", "skin_flexures"],
        severity_levels=["moderate", "severe"],
        common_duration="weeks to months",
        triggers=["autoimmune"],
        common_treatments=["corticosteroids", "immunosuppressants"],
        notes="A chronic autoimmune disease that causes large, fluid-filled blisters. More common in the elderly.",
    ),
    DiseaseInfo(
        name="Scabies",
        common_symptoms={
            "intense_itching": "high",
            "worse_at_night": "high",
            "rash_with_burrows": "high",
            "pimple_like_bumps": "medium",
        },
        age_min=0,
        age_max=100,
        common_locations=["between_fingers", "wrists", "waist", "armpits"],
        severity_levels=["mild", "moderate", "severe"],
        common_duration="chronic until treated",
        triggers=["infestation_by_mite", "close_contact"],
        common_treatments=["topical permethrin", "oral ivermectin"],
        notes="Highly contagious parasitic skin infestation. The intense itching is due to an allergic reaction to the mites.",
    ),
    DiseaseInfo(
        name="Lyme Disease",
        common_symptoms={
            "bulls_eye_rash": "high",
            "fever": "medium",
            "fatigue": "medium",
            "joint_pain": "medium",
        },
        age_min=0,
        age_max=100,
        common_locations=["site_of_tick_bite", "arms", "legs", "torso"],
        severity_levels=["mild", "moderate", "severe"],
        common_duration="weeks to months (if untreated)",
        triggers=["tick_bite"],
        common_treatments=["oral_antibiotics (doxycycline)"],
        notes="The initial rash (erythema migrans) is a key diagnostic sign. Can lead to chronic issues if not treated early.",
    ),
    DiseaseInfo(
        name="Drug-Induced Rash (Morbilliform)",
        common_symptoms={"symmetrical_red_rash": "high", "macules_and_papules": "high"},
        age_min=0,
        age_max=100,
        common_locations=["trunk", "arms", "legs"],
        severity_levels=["mild", "moderate"],
        common_duration="1-2 weeks",
        triggers=["medications (antibiotics, nsaids)"],
        common_treatments=[
            "stop_causative_drug",
            "antihistamines",
            "topical_corticosteroids",
        ],
        notes="Most common type of drug eruption. Usually appears 7-14 days after starting a new medication.",
    ),
    DiseaseInfo(
        name="Actinic Keratosis",
        common_symptoms={
            "rough_scaly_patch": "high",
            "sandpaper_feel": "high",
            "pink_or_red_spot": "medium",
        },
        age_min=50,
        age_max=100,
        common_locations=["face", "ears", "scalp", "hands", "forearms"],
        severity_levels=["mild"],
        common_duration="chronic",
        triggers=["chronic_sun_exposure"],
        common_treatments=[
            "cryotherapy",
            "topical_chemotherapy",
            "photodynamic_therapy",
        ],
        notes="A pre-cancerous lesion that can progress to Squamous Cell Carcinoma if left untreated.",
    ),
    DiseaseInfo(
        name="Basal Cell Carcinoma",
        common_symptoms={
            "pearly_bump": "high",
            "sore_that_wont_heal": "high",
            "visible_blood_vessels": "medium",
            "oozing_or_crusting": "medium",
        },
        age_min=50,
        age_max=100,
        common_locations=["face", "ears", "neck", "scalp", "hands"],
        severity_levels=["moderate"],
        common_duration="chronic and slow-growing",
        triggers=["long_term_sun_exposure"],
        common_treatments=["excision", "mohs_surgery", "cryotherapy"],
        notes="Most common type of skin cancer. It is slow-growing and rarely metastasizes.",
    ),
    DiseaseInfo(
        name="Squamous Cell Carcinoma",
        common_symptoms={
            "persistent_scaly_patch": "high",
            "wart_like_growth": "medium",
            "sore_that_wont_heal": "high",
            "raised_lesion_with_central_depression": "medium",
        },
        age_min=50,
        age_max=100,
        common_locations=["face", "ears", "lips", "scalp", "hands"],
        severity_levels=["moderate", "severe"],
        common_duration="chronic",
        triggers=["chronic_sun_exposure", "actinic_keratosis"],
        common_treatments=["excision", "mohs_surgery", "radiation"],
        notes="Second most common skin cancer. Has a higher potential to metastasize than Basal Cell Carcinoma.",
    ),
    DiseaseInfo(
        name="Melanoma",
        common_symptoms={
            "asymmetry": "high",
            "border_irregularity": "high",
            "color_variation": "high",
            "diameter_greater_than_6mm": "high",
            "evolution_of_mole": "high",
        },
        age_min=30,
        age_max=80,
        common_locations=["back", "legs", "arms", "face"],
        severity_levels=["severe"],
        common_duration="persistent/chronic",
        triggers=["uv_radiation", "genetic_factors", "multiple_atypical_moles"],
        common_treatments=["surgical_excision", "immunotherapy", "targeted_therapy"],
        notes="The most serious type of skin cancer due to its high potential for metastasis. Early detection is critical.",
    ),
]

DURATION_OPTIONS = [
    "1-2 weeks",
    "1-3 weeks",
    "2-4 weeks",
    "weeks to months",
    "months to years",
    "chronic",
    "chronic with flares",
]

DURATION_MAPPING = {
    "1-2 weeks": ["1-2 weeks"],
    "1-3 weeks": ["1-3 weeks"],
    "2-4 weeks": ["2-4 weeks", "days to weeks"],
    "weeks to months": ["weeks to months", "1-4 weeks"],
    "months to years": ["months to years", "6-12 months"],
    "chronic": ["chronic", "persistent/chronic", "chronic until treated", "persistent"],
    "chronic with flares": ["chronic with flares"],
}


def create_disease_lookup():
    """Creates a dictionary for efficient lookup of disease info by name."""
    return {d["name"]: d for d in diseases}
