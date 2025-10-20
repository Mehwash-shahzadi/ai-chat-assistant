import os
from huggingface_hub import InferenceClient

# Initialize client
client = InferenceClient(token=os.getenv("HUGGINGFACE_API_KEY"))

# ==========================================
# DAY 1: BASIC PROMPT - ASK QUESTIONS
# ==========================================

def ask_question(question):
  
    print(f"\n🔄 Processing question...")
    
    # Use chat_completion for conversational models
    response = client.chat_completion(
        model="mistralai/Mistral-7B-Instruct-v0.2",
        messages=[
            {
                "role": "user",
                "content": question
            }
        ],
        max_tokens=200,
        temperature=0.7
    )
    
    # Extract the text from response
    return response.choices[0].message.content


# ==========================================
# DAY 2: ADVANCED PROMPT - SUMMARIZE TEXT
# ==========================================

def summarize_text(text):
 
    print(f"\n🔄 Generating summary...")
    
    # Create summarization prompt with clear instructions
    prompt = f"""Summarize the following text in 2-3 sentences:{text} summarize:"""
    
    response = client.chat_completion(
        model="mistralai/Mistral-7B-Instruct-v0.2",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=150,  # Shorter for summaries
        temperature=0.5   # Lower temperature for focused output
    )
    
    return response.choices[0].message.content


# ==========================================
# EXERCISES
# ==========================================

if __name__ == "__main__":
    print("="*60)
    print("DAY 1 EXERCISE: ASK QUESTIONS")
    print("="*60)
    
    # Exercise 1.1: What is Python?
    question1 = "What is Python?"
    print(f"\n❓ Question: {question1}")
    answer1 = ask_question(question1)
    print(f"✅ Answer: {answer1}")
    

    print("\n" + "="*60)
    print("DAY 2 EXERCISE: SUMMARIZE TEXT")
    print("="*60)
    
    # Exercise 2.1: Summarize Python text
    long_text1 = """
    Python is a high-level, interpreted programming language known for its 
    simplicity and readability. Created by Guido van Rossum and first released 
    in 1991, Python emphasizes code readability with its notable use of 
    significant indentation. Python supports multiple programming paradigms, 
    including structured, object-oriented, and functional programming. It has 
    a comprehensive standard library and is widely used in web development, 
    data science, artificial intelligence, scientific computing, and automation. 
    Python's popularity has grown significantly due to its ease of learning, 
    extensive libraries like NumPy, Pandas, and TensorFlow, and its strong 
    community support.
    """
    
    print(f"\n📄 Original Text:\n{long_text1.strip()}")
    summary1 = summarize_text(long_text1)
    print(f"\n📝 Summary: {summary1}")