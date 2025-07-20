import json
import sys
import collections
import collections.abc
from experta import *
from ExpertSystem.engine import DermatologyExpert
from ExpertSystem.Questions.question_flow import apply_question_flow
from ExpertSystem.Questions.diagnosis import apply_diagnostic_rules
from ExpertSystem.facts import Answer
from gui import ModernFreshDermatologyGUI

collections.Mapping = collections.abc.Mapping


def cli_main():
    try:
        raw_input = sys.stdin.read()
        if not raw_input:
            print(json.dumps({"error": "No JSON input provided."}))
            return

        data = json.loads(raw_input)
        DermatologyExpertWithLogic = apply_question_flow(DermatologyExpert)
        DermatologyExpertWithLogic = apply_diagnostic_rules(DermatologyExpertWithLogic)

        engine = DermatologyExpertWithLogic()
        engine.reset()

        if "answers" in data and isinstance(data["answers"], dict):
            for key, val in data["answers"].items():
                engine.declare(Answer(ident=key, text=val))

        engine.run()

        if engine.best_diagnosis:
            final_diagnosis = engine.best_diagnosis
            result = {
                "disease": final_diagnosis.get("disease"),
                "reasoning": final_diagnosis.get("reasoning"),
                "confidence": final_diagnosis.get("cf"),
            }
            print(json.dumps(result, indent=2))
        else:
            print(json.dumps({"error": "No confident diagnosis could be made."}))

    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON format."}))
    except Exception as e:
        print(json.dumps({"error": f"An unexpected error occurred: {str(e)}"}))


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        cli_main()
    else:
        print("Starting Dermatology Expert System GUI...")
        DermatologyExpertWithLogic = apply_question_flow(DermatologyExpert)
        DermatologyExpertWithLogic = apply_diagnostic_rules(DermatologyExpertWithLogic)
        app = ModernFreshDermatologyGUI(DermatologyExpertWithLogic)
        app.run()


if __name__ == "__main__":
    main()
