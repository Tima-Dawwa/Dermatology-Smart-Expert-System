import json
import sys
import collections
import collections.abc
from experta import *  # Make sure experta is imported here for base classes

# Import the base DermatologyExpert
from ExpertSystem.engine import DermatologyExpert
# Import your rule application functions
from ExpertSystem.Questions.question_flow import apply_question_flow
from ExpertSystem.Questions.diagnosis import apply_diagnostic_rules

# Import your GUI application class
from ExpertSystem.facts import Answer
from gui import ModernFreshDermatologyGUI

collections.Mapping = collections.abc.Mapping  # Ensure compatibility for Experta


# You can keep the cli_main if you still want CLI functionality
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

        # Apply the logic to the base DermatologyExpert class
        DermatologyExpertWithLogic = apply_question_flow(DermatologyExpert)
        DermatologyExpertWithLogic = apply_diagnostic_rules(
            DermatologyExpertWithLogic)

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


def main():
    """Main function to run the application."""
    # This block determines whether to run in interactive (GUI) or CLI mode.
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        cli_main()
    else:
        # --- Interactive (GUI) Mode ---
        print("Starting Dermatology Expert System GUI...")

        # 1. Dynamically apply the rules to the base DermatologyExpert class
        # This creates the full rule-set for the GUI to use.
        DermatologyExpertWithLogic = apply_question_flow(DermatologyExpert)
        DermatologyExpertWithLogic = apply_diagnostic_rules(
            DermatologyExpertWithLogic)

        # 2. Instantiate your GUI, passing the *augmented* Expert class
        app = ModernFreshDermatologyGUI(DermatologyExpertWithLogic)

        # 3. Start the Tkinter event loop
        app.run()


if __name__ == "__main__":
    main()
