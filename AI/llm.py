import os
from huggingface_hub import InferenceClient




def explain_result_with_llm(result_text: str) -> str:
    prompt = f"""You are a helpful assistant that explains medical diagnoses to patients.

Your task is to convert the structured diagnostic output into a friendly, clear explanation suitable for a patient with no medical background.

Follow these rules:
- DO NOT include any internal thoughts or "<think>" tags.
- DO NOT describe your reasoning.
- Use the diagnosis name once, and explain it in simple terms.
- Include the confidence value exactly as given, e.g. "with a confidence of 78.8%".
- Use calm, reassuring tone.
- Limit your explanation to a single paragraph (2–3 sentences max).

Here is the input:
{result_text}\nExplanation:"""

    try:
        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.7,
            top_p=0.9,
            n=1,
        )
        explanation = completion.choices[0].message.content.strip()
        explanation = clean_explanation(explanation)
        return explanation

    except Exception as e:
        print(f"Error during generation: {e}")
        return "Sorry, I couldn't generate an explanation."


def clean_explanation(raw_output: str) -> str:
    if "</think>" in raw_output:
        cleaned = raw_output.split("</think>", 1)[1].strip()
        return cleaned
    else:
        return raw_output.strip()


if __name__ == "__main__":
    test_result = """


📋 Primary Diagnosis: Lipoma
    Confidence: 78.8%
    Reasoning: Soft lump is characteristic of lipoma.
    """
    explanation = explain_result_with_llm(test_result)
    print("\nGenerated Explanation:\n", explanation)
