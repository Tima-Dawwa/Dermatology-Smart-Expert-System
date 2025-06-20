import sys
import argparse
from ExpertSystem.facts import *
from ExpertSystem.engine import DermatologyExpert
from ExpertSystem.Questions.question_flow import apply_question_flow
from ExpertSystem.Questions.diagnosis import apply_diagnostic_rules
from AI.llm import MeditronLLM, DiagnosisResult, process_diagnosis_with_llm
import json
import collections
import collections.abc
from experta import *

collections.Mapping = collections.abc.Mapping


def cli_main(use_llm=False, include_explanation=False):
    """
    Runs the expert system in a non-interactive, command-line mode.
    Reads answers from a JSON input and prints a JSON output.
    
    Args:
        use_llm: Whether to use LLM for explanations
        include_explanation: Whether to include the full LLM explanation in JSON output
    """
    try:
        raw_input = sys.stdin.read()
        if not raw_input:
            print(json.dumps({"error": "No JSON input provided."}))
            return

        data = json.loads(raw_input)

        # Initialize LLM if requested
        llm_instance = None
        if use_llm:
            llm_instance = MeditronLLM()
            if not llm_instance.test_connection():
                print(json.dumps({"error": "LLM service is not available"}))
                return

        # Apply the logic to the class
        DermatologyExpertWithLogic = apply_question_flow(DermatologyExpert)
        DermatologyExpertWithLogic = apply_diagnostic_rules(
            DermatologyExpertWithLogic)

        # Create engine with LLM support
        engine = DermatologyExpertWithLogic(
            use_llm=use_llm, llm_instance=llm_instance)
        engine.reset()

        # Declare all answers provided in the JSON input
        if "answers" in data and isinstance(data["answers"], dict):
            for key, val in data["answers"].items():
                engine.declare(Answer(ident=key, text=val))
                # Store answers for LLM processing
                engine.patient_answers[key] = val

        engine.run()

        # Prepare the basic result
        if engine.best_diagnosis:
            final_diagnosis = engine.best_diagnosis
            result = {
                "disease": final_diagnosis.get("disease"),
                "reasoning": final_diagnosis.get("reasoning"),
                "confidence": final_diagnosis.get("cf"),
                "confidence_percentage": final_diagnosis.get("cf") * 100
            }

            # Add LLM explanation if requested
            if use_llm and include_explanation:
                explanation = engine.get_llm_explanation_only()
                if explanation:
                    result["ai_explanation"] = {
                        "detailed_explanation": explanation.detailed_explanation,
                        "causes": explanation.causes,
                        "symptoms_analysis": explanation.symptoms_analysis,
                        "treatment_recommendations": explanation.treatment_recommendations,
                        "prognosis": explanation.prognosis,
                        "when_to_seek_help": explanation.when_to_seek_help
                    }
                else:
                    result["ai_explanation"] = "LLM explanation could not be generated"

            print(json.dumps(result, indent=2))
        else:
            print(json.dumps(
                {"error": "No confident diagnosis could be made."}))

    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON format."}))
    except Exception as e:
        print(json.dumps({"error": f"An unexpected error occurred: {str(e)}"}))


def interactive_main(use_llm=True):
    """
    Runs the expert system in interactive mode.
    
    Args:
        use_llm: Whether to use LLM for explanations
    """
    # Initialize LLM if requested
    llm_instance = None
    if use_llm:
        print("🤖 Initializing AI explanation system...")
        llm_instance = MeditronLLM()
        if not llm_instance.test_connection():
            print("⚠️  Warning: AI explanation service is not available.")
            print(
                "    The expert system will still work but without detailed AI explanations.")
            use_llm = False
            llm_instance = None
        else:
            print("✅ AI explanation system ready!")

    # Apply the logic to the class
    DermatologyExpertWithLogic = apply_question_flow(DermatologyExpert)
    DermatologyExpertWithLogic = apply_diagnostic_rules(
        DermatologyExpertWithLogic)

    # Instantiate and run the engine
    engine = DermatologyExpertWithLogic(
        use_llm=use_llm, llm_instance=llm_instance)

    print("\n" + "="*60)
    print("🏥 DERMATOLOGY EXPERT SYSTEM")
    if use_llm:
        print("🤖 Enhanced with AI-powered explanations")
    print("="*60)
    print("Please answer the following questions to get a preliminary diagnosis.")
    print("="*60)

    engine.reset()
    engine.run()

    # The engine's display_results rule will handle showing results and LLM explanations


def main():
    """Main function with command line argument parsing"""
    parser = argparse.ArgumentParser(description='Dermatology Expert System')
    parser.add_argument('--cli', action='store_true',
                        help='Run in CLI mode (JSON input/output)')
    parser.add_argument('--no-llm', action='store_true',
                        help='Disable LLM explanations')
    parser.add_argument('--include-explanation', action='store_true',
                        help='Include full LLM explanation in CLI JSON output')

    args = parser.parse_args()

    use_llm = not args.no_llm

    if args.cli:
        cli_main(use_llm=use_llm, include_explanation=args.include_explanation)
    else:
        interactive_main(use_llm=use_llm)


if __name__ == '__main__':
    main()


# Example usage:
"""
Interactive mode with LLM:
python app.py

Interactive mode without LLM:
python app.py --no-llm

CLI mode with basic output:
echo '{"answers": {"age": "25", "duration": "chronic"}}' | python app.py --cli

CLI mode with LLM explanation:
echo '{"answers": {"age": "25", "duration": "chronic"}}' | python app.py --cli --include-explanation
"""
