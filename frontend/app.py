import streamlit as st
import requests
import time

# ============================================================================
# API CONFIGURATION
# ============================================================================
API_URL = "http://localhost:8000"

# ============================================================================
# API HELPER FUNCTIONS
# ============================================================================

def check_api_health():
    """Check if backend API is running"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def get_models():
    """Get available models from API"""
    try:
        response = requests.get(f"{API_URL}/models", timeout=5)
        data = response.json()
        return data["models"], data["current"]
    except Exception as e:
        st.error(f"❌ Error getting models: {e}")
        return [], "mistral"

def switch_model(model_name):
    """Switch AI model via API"""
    try:
        response = requests.post(
            f"{API_URL}/switch-model",
            json={"model_name": model_name},
            timeout=5
        )
        return response.json()["message"]
    except Exception as e:
        return f"Error: {e}"

def generate_response(prompt, max_tokens):
    """Generate AI response via API"""
    try:
        response = requests.post(
            f"{API_URL}/query",
            json={"prompt": prompt, "max_tokens": max_tokens},
            timeout=60  # AI can take time
        )
        data = response.json()
        return data["response"]
    except Exception as e:
        return f"❌ Error: {e}"

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'process_question' not in st.session_state:
    st.session_state.process_question = None
if 'current_model' not in st.session_state:
    st.session_state.current_model = "mistral"

# ============================================================================
# SYSTEM PROMPT
# ============================================================================

SYSTEM_PROMPT = """Keep your answer SHORT (2-3 sentences max). Be helpful and friendly. Use 1-2 emojis. Get straight to the point."""

def create_enhanced_prompt(user_message):
    """Create optimized prompt for short answers"""
    return f"{SYSTEM_PROMPT}\n\nQuestion: {user_message}\n\nAnswer:"

def process_user_question(question, max_tokens):
    """Process a question and generate response via API"""
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": question})
    
    # Create enhanced prompt
    enhanced_prompt = create_enhanced_prompt(question)
    
    # Get response from API (not direct LLMService!)
    response = generate_response(enhanced_prompt, max_tokens)
    
    # Clean response
    response = response.strip()
    
    # Add AI response to history
    st.session_state.messages.append({"role": "assistant", "content": response})

# ============================================================================
# CHECK API CONNECTION
# ============================================================================

# Check if backend is running
if not check_api_health():
    st.error("⚠️ **Backend API is not running!**")
    st.info("""
    **To start the backend:**
    1. Open a new terminal
    2. Activate your virtual environment
    3. Run: `uvicorn backend.main:app --reload`
    4. Then refresh this page
    """)
    st.stop()

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    # Branding
    st.markdown("# 🤖 AI Assistant")
    st.success("✨ Free & Open Source")
    st.caption("Powered by HuggingFace")
    st.markdown("---")
    
    # AI Model Selection
    st.markdown("**🤖 AI Model**")
    
    # Get models from API
    available_models, current_model = get_models()
    st.session_state.current_model = current_model
    
    model_info = {
        "mistral": "⚡ Fast & Smart",
        "zephyr": "💬 Best for Chat",
        "llama": "🧠 Advanced AI"
    }
    
    selected_model = st.selectbox(
        "model",
        available_models,
        index=available_models.index(current_model) if current_model in available_models else 0,
        format_func=lambda x: f"{x.title()} {model_info.get(x, '')}",
        label_visibility="collapsed",
        key="model_selector"
    )
    
    # Switch model if changed
    if selected_model != st.session_state.current_model:
        result = switch_model(selected_model)
        st.success(f"✅ {result}")
        st.session_state.current_model = selected_model
        st.rerun()
    
    st.markdown("---")
    
    # Response Length
    st.markdown("**📏 Response Length**")
    max_tokens = st.select_slider(
        "tokens",
        options=[50, 100, 150, 200, 250, 300],
        value=150,
        label_visibility="collapsed",
        key="token_slider"
    )
    st.caption(f"**Current:** {max_tokens} tokens")
    
    st.markdown("---")
    
    # Clear Chat Button
    if st.button("🗑️ Clear Chat", use_container_width=True, type="primary", key="clear_btn"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    
    # Stats Section
    st.markdown("### 📊 Stats")
    
    total_messages = len(st.session_state.messages)
    
    stat_col1, stat_col2 = st.columns(2)
    with stat_col1:
        st.metric("💬 Messages", total_messages)
    with stat_col2:
        st.metric("🤖 Model", st.session_state.current_model.upper()[:3])
    
    st.markdown("---")
    
    # Guide Section
    st.markdown("### 📖 Guide")
    
    with st.expander("🚀 Quick Start"):
        st.markdown("""
        **Get started in 3 steps:**
        
        1️⃣ Type your question in chat
        2️⃣ Press Enter to send
        3️⃣ Get instant AI response!
        
        💡 Try quick action buttons!
        """)
    
    with st.expander("💡 Example Questions"):
        st.markdown("""
        - What is Python?
        - Explain AI simply
        - Give me a coding tip
        - Tell me an interesting fact
        """)
    
    with st.expander("🤖 About Models"):
        st.markdown("""
        **Mistral** ⚡ - Fast & accurate
        **Zephyr** 💬 - Conversational
        **Llama** 🧠 - Advanced reasoning
        """)
    
    # Footer
    st.markdown("---")
    st.caption("v1.0 | Backend: FastAPI")

# ============================================================================
# MAIN CHAT AREA
# ============================================================================

st.title("🤖 AI Chat Assistant")
st.caption("Ask me anything - I'll keep it short & helpful! ✨")

# ============================================================================
# QUICK ACTIONS
# ============================================================================

if len(st.session_state.messages) == 0:
    st.markdown("---")
    st.markdown("### ⚡ Quick Start")
    st.caption("Click any button to start:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💡 Interesting Fact", use_container_width=True, key="fact_btn"):
            st.session_state.process_question = "Tell me an interesting fact about technology"
        
        if st.button("🎯 Coding Tip", use_container_width=True, key="tip_btn"):
            st.session_state.process_question = "Give me a quick coding tip"
    
    with col2:
        if st.button("😄 Programming Joke", use_container_width=True, key="joke_btn"):
            st.session_state.process_question = "Tell me a programming joke"
        
        if st.button("🧠 AI Concept", use_container_width=True, key="ai_btn"):
            st.session_state.process_question = "Explain one AI concept simply"
    
    st.info("💡 **Tip:** Type your own question below or click a button!")
    st.markdown("---")

# Process question from button
if st.session_state.process_question:
    with st.spinner("💭 Thinking..."):
        process_user_question(st.session_state.process_question, max_tokens)
    st.session_state.process_question = None
    st.rerun()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Ask me anything...", key="chat_input")

if user_input:
    with st.spinner("💭 Thinking..."):
        process_user_question(user_input, max_tokens)
    st.rerun()

# Footer
st.markdown("---")
st.caption("Made with ❤️ using Streamlit & HuggingFace | © 2025")