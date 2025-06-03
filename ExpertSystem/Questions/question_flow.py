from experta import Rule, Fact, MATCH, NOT
from ExpertSystem.facts import Answer


def apply_question_flow(cls):
    @Rule(NOT(Answer(ident="age")), salience=100)
    def start_with_age(self):
        self.declare(Fact(next="age"))
    cls.start_with_age = start_with_age

    flow_sequence = [
        "age",
        "symptom_duration",
        "itching",
        ("itching", {"yes": "dryness", "no": "scaling"}),
        ("dryness", {"yes": "redness", "no": "scaling"}),
        ("scaling", {"yes": "redness", "no": "redness"}),
        "redness",
        "blisters",
        "pain",
        "ulcer",
        "discoloration",
        "joint_pain",
        "bleeding",
        "enlarging_rapidly",
        "mucosal_involvement",
        "sun_exposure_area",
        "rash_shape",
        "rash_between_fingers",
        "rash_scalp",
        "oozing_crusting",
        "vesicles",
        "hair_loss",
        "nail_changes",
        "photosensitivity",
        "hives",
        "fever_rash",
        "drug_history",
        "contact_history",
        "skin_lightening",
        "burning_sensation",
        "weight_loss",
        "night_sweats",
        "autoimmune_history",
        "acne",
        "rosacea",
        "rash_symmetry",
        "swelling",
        "history_cancer"
    ]

    def make_sequential_rule(prev, nxt):
        def rule_fn(self, response):
            self.declare(Fact(next=nxt))
        rule_name = f"rule_{prev}_to_{nxt}"
        rule_fn.__name__ = rule_name
        setattr(cls, rule_name, Rule(
            Answer(ident=prev, text=MATCH.response))(rule_fn))

    def make_conditional_rule(symptom, outcomes):
        for val, nxt in outcomes.items():
            def rule_fn(self, val=val, nxt=nxt):
                self.declare(Fact(next=nxt))
            rule_name = f"rule_{symptom}_{val}_to_{nxt}"
            rule_fn.__name__ = rule_name
            setattr(cls, rule_name, Rule(
                Answer(ident=symptom, text=val))(rule_fn))

    for i, step in enumerate(flow_sequence[:-1]):
        if isinstance(step, tuple):
            symptom, outcomes = step
            make_conditional_rule(symptom, outcomes)
        else:
            next_step = flow_sequence[i + 1]
            if not isinstance(next_step, tuple):
                make_sequential_rule(step, next_step)

    # Final rule
    @Rule(Answer(ident="history_cancer", text=MATCH.response))
    def end_of_flow(self, response):
        self.declare(Fact(next=None))
    cls.end_of_flow = end_of_flow
