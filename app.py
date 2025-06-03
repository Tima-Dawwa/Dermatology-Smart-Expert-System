import sys
from ExpertSystem.facts import *
from ExpertSystem.engine import DermatologyExpert
import json
import collections
import collections.abc
from experta import *

collections.Mapping = collections.abc.Mapping


def cli_main():
    try:
        raw_input = sys.stdin.read()
        data = json.loads(raw_input)

        engine = DermatologyExpert()
        engine.reset()

        for key, val in data["answers"].items():
            engine.declare(Fact(ask=key))
            engine.declare(Answer(ident=key, text=val))

        if "cv" in data:
            cv = data["cv"]
            engine.declare(ImageDiagnosis(
                disease=cv["disease"], confidence=cv["confidence"]))

        engine.run()

        for fact in engine.facts.values():
            if isinstance(fact, Diagnosis):
                result = {
                    "disease": fact["disease"],
                    "reasoning": fact["reasoning"],
                    "confidence": fact["cf"]
                }
                print(json.dumps(result))
                return

        print(json.dumps({"error": "No confident diagnosis"}))

    except Exception as e:
        print(json.dumps({"error": str(e)}))


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        cli_main()
    else:
        engine = DermatologyExpert()
        engine.reset()
        engine.declare(Fact(next='itching'))
        engine.run()
        engine.get_final_diagnosis()
