import os
from huggingface_hub import InferenceClient


def explain_result_with_llm(result_text: str) -> str:
    """
    Generate a user-friendly explanation for the given result by calling DeepSeek-R1 model
    via Hugging Face Inference API.

    Args:
        result_text (str): The raw output from the expert system.

    Returns:
        str: A simplified explanation generated by the LLM.
    """
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
            messages=[
                {"role": "user", "content": prompt}
            ],
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
        # Split on '</think>' and take the part after it
        cleaned = raw_output.split("</think>", 1)[1].strip()
        return cleaned
    else:
        # No internal reasoning tags found, return as is
        return raw_output.strip()


# ======== TEST (optional) ========
if __name__ == "__main__":
    test_result = """


📋 Primary Diagnosis: Lipoma
    Confidence: 78.8%
    Reasoning: Soft lump is characteristic of lipoma.
    """
    explanation = explain_result_with_llm(test_result)
    print("\nGenerated Explanation:\n", explanation)
