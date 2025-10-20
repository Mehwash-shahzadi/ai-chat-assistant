from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()

def test_prompt_engineering():
    hf_token = os.getenv("HUGGINGFACE_API_TOKEN")
    if not hf_token:
        raise RuntimeError("Set HUGGINGFACE_API_TOKEN environment variable before running.")

    client = InferenceClient(token=hf_token)

    prompts = {
        "basic": "What is Python?",
        "detailed": "Explain Python programming language in simple terms for beginners.",
        "structured": "You are a helpful coding tutor. Explain Python to a beginner in 3 bullet points.",
    }

    for style, prompt in prompts.items():
        print("\n" + "="*50)
        print(f"Testing {style.upper()} prompt:")
        print(f"Prompt: {prompt}")
        print("="*50)

        try:
            response = client.chat_completion(
                model="mistralai/Mistral-7B-Instruct-v0.2",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
            )
            print(response.choices[0].message["content"])
        except Exception as e:
            print("Request failed:", e)
            continue

if __name__ == "__main__":
    test_prompt_engineering()
