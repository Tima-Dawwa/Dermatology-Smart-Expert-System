from experta import *
from ExpertSystem.facts import Answer, Stop, Diagnosis


def apply_diagnostic_rules(cls):
    """
    This function applies all 37 diagnostic rules to the KnowledgeEngine class.
    """

    # --- Branch A Diagnoses ---
    @Rule(NOT(Stop()), Answer(ident='has_symptom_lump_or_growth', text='yes'), Answer(ident='has_symptom_soft_lump', text='yes'))
    def diagnose_lipoma(self): self.declare_or_update_diagnosis(
        disease="Lipoma",
        reasoning="Soft lump is characteristic of lipoma.",
        new_cf=0.8
    )
    cls.diagnose_lipoma = diagnose_lipoma

    @Rule(NOT(Stop()), Answer(ident='has_symptom_lump_or_growth', text='yes'), Answer(ident='has_symptom_firm_lump', text='yes'))
    def diagnose_dermatofibroma(self): self.declare_or_update_diagnosis(
        disease="Dermatofibroma",
        reasoning="Firm lump is characteristic of dermatofibroma.",
        new_cf=0.8
    )
    cls.diagnose_dermatofibroma = diagnose_dermatofibroma

    @Rule(NOT(Stop()), Answer(ident='has_symptom_lump_or_growth', text='yes'), Answer(ident='has_symptom_rough_bumps', text='yes'))
    def diagnose_warts(self): self.declare_or_update_diagnosis(
        disease="Warts (Verruca Vulgaris)",
        reasoning="Bumps suggest warts.",
        new_cf=0.7
    )
    cls.diagnose_warts = diagnose_warts

    # here
    @Rule(NOT(Stop()), Answer(ident='has_symptom_sore_that_wont_heal', text='yes'), Answer(ident='has_symptom_persistent_scaly_patch', text='no'))
    def diagnose_bcc(self): self.declare_or_update_diagnosis(
        disease='Basal Cell Carcinoma',
        reasoning="A Sore that wont heal but without scaly patches", cf=0.9)
    cls.diagnose_bcc = diagnose_bcc

    @Rule(NOT(Stop()), Answer(ident='has_symptom_lump_or_growth', text='yes'), Answer(ident='has_symptom_waxy_appearance', text='yes'))
    def diagnose_seborrheic_keratosis(self): self.declare_or_update_diagnosis(
        disease="Seborrheic Keratoses",
        reasoning="Waxy appearance with scaling suggests seborrheic keratoses.",
        new_cf=0.8
    )
    cls.diagnose_seborrheic_keratosis = diagnose_seborrheic_keratosis

    @Rule(NOT(Stop()), Answer(ident='has_symptom_lump_or_growth', text='yes'), Answer(ident='has_symptom_evolution_of_mole', text='yes'))
    def diagnose_melanoma(self): self.declare_or_update_diagnosis(
        disease="Melanoma Skin Cancer",
        reasoning="Discoloration with ulcer and bleeding may indicate melanoma.",
        new_cf=0.85
    )
    cls.diagnose_melanoma = diagnose_melanoma

    # here
    @Rule(NOT(Stop()), Answer(ident='has_symptom_sore_that_wont_heal', text='yes'), Answer(ident='has_symptom_persistent_scaly_patch', text='yes'))
    def diagnose_scc(self): self.declare_or_update_diagnosis(
        disease='Squamous Cell Carcinoma',
        reasoning="a sore that wont heal and also scaly patches", cf=0.95)
    cls.diagnose_scc = diagnose_scc

    # --- Branch B Diagnoses ---
    @Rule(NOT(Stop()), Answer(ident='affects_nails_or_hair', text='yes'), Answer(ident='has_symptom_patchy_hair_loss', text='yes'))
    def diagnose_alopecia_areata(self): self.declare_or_update_diagnosis(
        disease="Alopecia Areata",
        reasoning="Hair thinning with patchy baldness is characteristic of alopecia.",
        new_cf=0.85
    )
    cls.diagnose_alopecia_areata = diagnose_alopecia_areata

    @Rule(NOT(Stop()), Answer(ident='affects_nails_or_hair', text='yes'), Answer(ident='has_symptom_nail_pitting', text='yes'))
    def diagnose_nail_psoriasis(self): self.declare_or_update_diagnosis(
        disease="Nail Psoriasis",
        reasoning="Nail pitting is characteristic of nail psoriasis.",
        new_cf=0.85
    )
    cls.diagnose_nail_psoriasis = diagnose_nail_psoriasis

    @Rule(NOT(Stop()), Answer(ident='affects_nails_or_hair', text='yes'), Answer(ident='has_symptom_nail_thickening', text='yes'))
    def diagnose_onychomycosis(self): self.declare_or_update_diagnosis(
        disease="Onychomycosis",
        reasoning="Nail thickening with discoloration is characteristic of nail fungus.",
        new_cf=0.85
    )
    cls.diagnose_onychomycosis = diagnose_onychomycosis

    @Rule(NOT(Stop()), Answer(ident='affects_nails_or_hair', text='yes'), Answer(ident='has_symptom_nail_concavity', text='yes'))
    def diagnose_koilonychia(self): self.declare_or_update_diagnosis(
        disease="Koilonychia (Spoon Nails)",
        reasoning="Nail concavity is characteristic of koilonychia.",
        new_cf=0.85
    )
    cls.diagnose_koilonychia = diagnose_koilonychia

    @Rule(NOT(Stop()), Answer(ident='affects_nails_or_hair', text='yes'), Answer(ident='has_symptom_nail_fold_swelling', text='yes'))
    def diagnose_paronychia(self): self.declare_or_update_diagnosis(
        disease="Paronychia",
        reasoning="Swelling, redness, and pain are characteristic of paronychia.",
        new_cf=0.85
    )
    cls.diagnose_paronychia = diagnose_paronychia

    @Rule(NOT(Stop()), Answer(ident='affects_nails_or_hair', text='yes'), Answer(ident='has_symptom_transverse_nail_grooves', text='yes'))
    def diagnose_beaus_lines(self): self.declare_or_update_diagnosis(
        disease="Beau's Lines",
        reasoning="Horizontal nail grooves indicate Beau's lines.",
        new_cf=0.8
    )
    cls.diagnose_beaus_lines = diagnose_beaus_lines

    # --- Branch C Diagnoses ---
    @Rule(NOT(Stop()), Answer(ident='has_symptom_rash', text='yes'), Answer(ident='has_symptom_itching', text='yes'), Answer(ident='has_symptom_worse_at_night', text='yes'))
    def diagnose_scabies(self): self.declare_or_update_diagnosis(
        disease="Scabies",
        reasoning="Itching rash that's worse at night is characteristic of scabies.",
        new_cf=0.9
    )
    cls.diagnose_scabies = diagnose_scabies

    @Rule(NOT(Stop()), Answer(ident='has_symptom_rash', text='yes'), Answer(ident='has_symptom_itching', text='yes'), Answer(ident='has_symptom_dryness', text='yes'))
    def diagnose_eczema(self): self.declare_or_update_diagnosis(
        disease="Eczema (Atopic Dermatitis)",
        reasoning="High itching with high dryness is characteristic of eczema.",
        new_cf=0.8
    )
    cls.diagnose_eczema = diagnose_eczema

    # here
    @Rule(NOT(Stop()), Answer(ident='has_symptom_ring_shaped_rash', text='yes'), Answer(ident='locations', text='feet'))
    def diagnose_tinea_pedis(self): self.declare_or_update_diagnosis(
        disease="Tinea Pedis (Athlete's Foot)",
        reasoning="Tinea Pedis usaully comes with a ring-shaped rash on the feet (for atheletes)", cf=0.9)
    cls.diagnose_tinea_pedis = diagnose_tinea_pedis

    @Rule(NOT(Stop()), Answer(ident='has_symptom_ring_shaped_rash', text='yes'), Answer(ident='locations', text='body'))
    def diagnose_tinea_corporis(self): self.declare_or_update_diagnosis(
        disease="Tinea (Ringworm)",
        reasoning="Ring-shaped rash with scaling suggests ringworm infection.",
        new_cf=0.85
    )
    cls.diagnose_tinea_corporis = diagnose_tinea_corporis

    @Rule(NOT(Stop()), Answer(ident='has_symptom_white_patches', text='yes'))
    def diagnose_candidiasis(self): self.declare_or_update_diagnosis(
        disease='Candidiasis',
        reasoning="Candidasis main symptom is white patches", cf=0.8)
    cls.diagnose_candidiasis = diagnose_candidiasis

    @Rule(NOT(Stop()), Answer(ident='trigger_contact_related', text='yes'))
    def diagnose_contact_dermatitis(self): self.declare_or_update_diagnosis(
        disease='Contact Dermatitis',
        reasoning="Contact Dermatitis is triggered by plants, metals, and new objects", cf=0.9)
    cls.diagnose_contact_dermatitis = diagnose_contact_dermatitis

    # here
    @Rule(NOT(Stop()), Answer(ident='has_symptom_large_tense_blisters', text='yes'))
    def diagnose_bullous_pemphigoid(self): self.declare_or_update_diagnosis(
        disease='Bullous Pemphigoid',
        reasoning="Large tense blisters are often a symptom of Bullous Pemphigoid", cf=0.9)
    cls.diagnose_bullous_pemphigoid = diagnose_bullous_pemphigoid

    @Rule(NOT(Stop()), Answer(ident='has_symptom_thick_patches', text='yes'))
    def diagnose_psoriasis(self): self.declare_or_update_diagnosis(
        disease="Nail Psoriasis",
        reasoning="Nail pitting is characteristic of nail psoriasis.",
        new_cf=0.85
    )
    cls.diagnose_psoriasis = diagnose_psoriasis

    # here
    @Rule(NOT(Stop()), Answer(ident='has_symptom_pimples', text='yes'))
    def diagnose_acne_vulgaris(self): self.declare_or_update_diagnosis(
        disease='Acne Vulgaris',
        reasoning="Usual Pimples are Acne", cf=0.85)
    cls.diagnose_acne_vulgaris = diagnose_acne_vulgaris

    @Rule(NOT(Stop()), Answer(ident='has_symptom_unilateral_rash', text='yes'), Answer(ident='has_symptom_pain', text='yes'))
    def diagnose_shingles(self): self.declare_or_update_diagnosis(
        disease="Herpes Zoster (Shingles)",
        reasoning="Painful rash with blisters is characteristic of shingles.",
        new_cf=0.85
    )
    cls.diagnose_shingles = diagnose_shingles

    @Rule(NOT(Stop()), Answer(ident='has_symptom_bulls_eye_rash', text='yes'))
    def diagnose_lyme_disease(self): self.declare_or_update_diagnosis(
        disease="Lyme Disease",
        reasoning="Rash with joint pain may indicate Lyme disease.",
        new_cf=0.75
    )
    cls.diagnose_lyme_disease = diagnose_lyme_disease

    @Rule(NOT(Stop()), Answer(ident='has_symptom_butterfly_rash', text='yes'))
    def diagnose_lupus(self): self.declare_or_update_diagnosis(
        disease="Lupus (Cutaneous)",
        reasoning="Rash with joint pain and photosensitivity suggests lupus.",
        new_cf=0.85
    )
    cls.diagnose_lupus = diagnose_lupus

    @Rule(NOT(Stop()), Answer(ident='has_symptom_painful_blisters', text='yes'))
    def diagnose_hsv(self): self.declare_or_update_diagnosis(
        disease="Herpes Simplex Virus (HSV)",
        reasoning="Painful blisters are characteristic of herpes simplex.",
        new_cf=0.8
    )
    cls.diagnose_hsv = diagnose_hsv

    @Rule(NOT(Stop()), Answer(ident='has_symptom_honey_colored_crusts', text='yes'))
    def diagnose_impetigo(self): self.declare_or_update_diagnosis(
        disease="Impetigo",
        reasoning="Blisters with crusting is characteristic of impetigo.",
        new_cf=0.85
    )
    cls.diagnose_impetigo = diagnose_impetigo

    @Rule(NOT(Stop()), Answer(ident='has_symptom_spreading_redness', text='yes'), Answer(ident='has_symptom_warmth', text='yes'))
    def diagnose_cellulitis(self): self.declare_or_update_diagnosis(
        disease="Cellulitis",
        reasoning="Redness, pain, swelling, and warmth indicate cellulitis infection.",
        new_cf=0.9
    )
    cls.diagnose_cellulitis = diagnose_cellulitis

    # here
    @Rule(NOT(Stop()), Answer(ident='has_symptom_symmetrical_red_rash', text='yes'), Answer(ident='trigger_medications', text='yes'))
    def diagnose_drug_rash(self): self.declare_or_update_diagnosis(
        disease='Drug-Induced Rash',
        reasoning="A symmetrical red-rash after new drugs or medicines can induce this rash", cf=0.8)
    cls.diagnose_drug_rash = diagnose_drug_rash

    # --- Branch D Diagnoses ---
    @Rule(NOT(Stop()), Answer(ident='has_symptom_palpable_purpura', text='yes'))
    def diagnose_vasculitis(self): self.declare_or_update_diagnosis(
        disease="Vasculitis",
        reasoning="Painful ulcer may indicate vasculitis.",
        new_cf=0.7
    )
    cls.diagnose_vasculitis = diagnose_vasculitis

    # here
    @Rule(NOT(Stop()), Answer(ident='has_symptom_loss_of_pigment', text='yes'))
    def diagnose_vitiligo(self): self.declare_or_update_diagnosis(
        disease='Vitiligo',
        reasoning="suddent loss of pigment of skin is Vitiligo", cf=0.9)
    cls.diagnose_vitiligo = diagnose_vitiligo

    # here
    @Rule(NOT(Stop()), Answer(ident='has_symptom_brown_or_gray_patches', text='yes'))
    def diagnose_melasma(self): self.declare_or_update_diagnosis(
        disease='Melasma',
        reasoning="brown or gray patches on the skin usually refers to Melasma", cf=0.85)
    cls.diagnose_melasma = diagnose_melasma

    @Rule(NOT(Stop()), Answer(ident='has_symptom_discolored_patches', text='yes'))
    def diagnose_tinea_versicolor(self): self.declare_or_update_diagnosis(
        disease="Tinea Versicolor",
        reasoning="High discoloration with scaling suggests tinea versicolor.",
        new_cf=0.8
    )
    cls.diagnose_tinea_versicolor = diagnose_tinea_versicolor

    @Rule(NOT(Stop()), Answer(ident='has_symptom_central_dimple', text='yes'))
    def diagnose_molluscum(self): self.declare_or_update_diagnosis(
        disease="Molluscum Contagiosum",
        reasoning="Bumps with central dimple are characteristic of molluscum contagiosum.",
        new_cf=0.9
    )
    cls.diagnose_molluscum = diagnose_molluscum

    # here
    @Rule(NOT(Stop()), Answer(ident='has_symptom_rough_scaly_patch', text='yes'))
    def diagnose_actinic_keratosis(self): self.declare_or_update_diagnosis(
        disease='Actinic Keratosis',
        reasoning="Rough and Scaly Patches are part of the Actinic Keratosis", cf=0.9)
    cls.diagnose_actinic_keratosis = diagnose_actinic_keratosis

    @Rule(NOT(Stop()), Answer(ident='has_symptom_persistent_redness', text='yes'))
    def diagnose_rosacea(self): self.declare_or_update_diagnosis(
        disease="Rosacea",
        reasoning="High redness with pimples is characteristic of acne or rosacea.",
        new_cf=0.85
    )
    cls.diagnose_rosacea = diagnose_rosacea

    @Rule(NOT(Stop()), salience=-1)
    def stop_engine_flag(self):
        self.declare(Stop())

    return cls
