import sys
from ExpertSystem.facts import *
from ExpertSystem.engine import DermatologyExpert
from ExpertSystem.Questions.question_flow import apply_question_flow
from ExpertSystem.Questions.diagnosis import apply_diagnostic_rules
import json
import collections
import collections.abc
from experta import *

collections.Mapping = collections.abc.Mapping


def cli_main():
    """
    Runs the expert system in a non-interactive, command-line mode.
    Reads answers from a JSON input and prints a JSON output.
    """
    try:
        raw_input = sys.stdin.read()
        if not raw_input:
            print(json.dumps({"error": "No JSON input provided."}))
            return

        data = json.loads(raw_input)

        # Apply the logic to the class
        DermatologyExpertWithLogic = apply_question_flow(DermatologyExpert)
        DermatologyExpertWithLogic = apply_diagnostic_rules(
            DermatologyExpertWithLogic)

        engine = DermatologyExpertWithLogic()
        engine.reset()

        # Declare all answers provided in the JSON input
        if "answers" in data and isinstance(data["answers"], dict):
            for key, val in data["answers"].items():
                engine.declare(Answer(ident=key, text=val))

        engine.run()

        # After the engine runs, access the 'best_diagnosis' property we added
        if engine.best_diagnosis:
            final_diagnosis = engine.best_diagnosis
            result = {
                "disease": final_diagnosis.get("disease"),
                "reasoning": final_diagnosis.get("reasoning"),
                "confidence": final_diagnosis.get("cf")
            }
            print(json.dumps(result, indent=2))
        else:
            print(json.dumps(
                {"error": "No confident diagnosis could be made."}))

    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON format."}))
    except Exception as e:
        print(json.dumps({"error": f"An unexpected error occurred: {str(e)}"}))


if __name__ == '__main__':
    # This block determines whether to run in interactive or CLI mode.
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        cli_main()
    else:
        # --- Interactive Mode ---
        # Apply the logic to the class
        DermatologyExpertWithLogic = apply_question_flow(DermatologyExpert)
        DermatologyExpertWithLogic = apply_diagnostic_rules(
            DermatologyExpertWithLogic)

        # Instantiate and run the engine
        engine = DermatologyExpertWithLogic()

        print("--- Starting Dermatology Expert System ---")
        print("Please answer the following questions.")

        engine.reset()
        engine.run()

     