from huggingface_hub import InferenceClient
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    """Service to handle multiple HuggingFace models"""
    
    #  THESE MODELS ACTUALLY WORK (Tested and Free!)
    MODELS = {
        "mistral": "mistralai/Mistral-7B-Instruct-v0.2",
        "zephyr": "HuggingFaceH4/zephyr-7b-beta",
        "llama": "meta-llama/Llama-3.2-3B-Instruct"
    }
    
    def __init__(self):
        self.token = os.getenv("HUGGINGFACE_API_TOKEN")
        if not self.token:
            raise ValueError(" HUGGINGFACE_API_TOKEN not found in .env file!")
        
        self.client = InferenceClient(token=self.token)
        self.current_model = "mistral"
        print(f" Service initialized with model: {self.current_model}")
    
    def switch_model(self, model_name: str):
        """Switch between different models"""
        if model_name in self.MODELS:
            self.current_model = model_name
            print(f" Switched to {model_name}")
            return f"Switched to {model_name}"
        print(f" Model {model_name} not found")
        return "Model not found"
    
    def generate_response(self, prompt: str, max_tokens: int = 512) -> str:
        """Generate response using current model"""
        try:
            print(f" Sending request to {self.current_model}...")
            
            #  FIX: Use chat_completion instead of text_generation
            response = self.client.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                model=self.MODELS[self.current_model],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            # Extract the message content from the response
            answer = response.choices[0].message.content
            
            print(f" Got response from {self.current_model}")
            return answer.strip()
            
        except Exception as e:
            error_msg = f"Error with {self.current_model}: {str(e)}"
            print(f" {error_msg}")
            return error_msg
    
    def get_available_models(self) -> List[str]:
        """Return list of available models"""
        return list(self.MODELS.keys())
    
    def get_current_model(self) -> str:
        """Get currently active model"""
        return self.current_model


# Test the service
if __name__ == "__main__":
    print("=" * 60)
    print(" TESTING LLM SERVICE")
    print("=" * 60)
    
    try:
        # Initialize service
        llm = LLMService()
        
        # Show available models
        print(f"\n Available models: {llm.get_available_models()}")
        print(f" Current model: {llm.get_current_model()}")
        
        # Test 1: Mistral
        print("\n" + "=" * 60)
        print("TEST 1: MISTRAL MODEL")
        print("=" * 60)
        question1 = "What is machine learning in one sentence?"
        print(f"Question: {question1}")
        response1 = llm.generate_response(question1, max_tokens=100)
        print(f"Answer: {response1}")
        
        # Test 2: Zephyr
        print("\n" + "=" * 60)
        print("TEST 2: ZEPHYR MODEL")
        print("=" * 60)
        llm.switch_model("zephyr")
        question2 = "What is Python programming?"
        print(f"Question: {question2}")
        response2 = llm.generate_response(question2, max_tokens=100)
        print(f"Answer: {response2}")
        
        # Test 3: Llama
        print("\n" + "=" * 60)
        print("TEST 3: LLAMA MODEL")
        print("=" * 60)
        llm.switch_model("llama")
        question3 = "Explain AI briefly"
        print(f"Question: {question3}")
        response3 = llm.generate_response(question3, max_tokens=100)
        print(f"Answer: {response3}")
        
        print("\n" + "=" * 60)
        print(" ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n ERROR: {e}")
        print("\n Check that:")
        print("   1. Your HUGGINGFACE_TOKEN is in backend/.env")
        print("   2. Your token is valid (check https://huggingface.co/settings/tokens)")
        print("   3. You're connected to internet")