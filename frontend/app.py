import streamlit as st
import requests
from auth_ui import show_login_page, logout

API_URL = "http://localhost:8000"

# Page config
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Functions
def check_api_health():
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def get_models(token):
    try:
        response = requests.get(
            f"{API_URL}/models",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
        data = response.json()
        return data["models"], data["current"]
    except:
        return [], "mistral"

def switch_model(model_name, token):
    try:
        response = requests.post(
            f"{API_URL}/switch-model",
            json={"model_name": model_name},
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
        return response.json()["message"]
    except Exception as e:
        return f"Error: {e}"

def generate_response(prompt, max_tokens, token):
    try:
        response = requests.post(
            f"{API_URL}/query",
            json={"prompt": prompt, "max_tokens": max_tokens},
            headers={"Authorization": f"Bearer {token}"},
            timeout=60
        )
        
        if response.status_code == 401:
            st.error(" Session expired")
            logout()
            return "Session expired"
        
        return response.json()["response"]
    except Exception as e:
        return f" Error: {e}"

# Session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'token' not in st.session_state:
    st.session_state.token = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'process_question' not in st.session_state:
    st.session_state.process_question = None
if 'current_model' not in st.session_state:
    st.session_state.current_model = "mistral"

# Check backend
if not check_api_health():
    st.error(" Backend API is not running!")
    st.info("**Start backend:** `uvicorn backend.main:app --reload`")
    st.stop()

# Check authentication
if not st.session_state.authenticated:
    show_login_page()
    st.stop()

# System prompt
SYSTEM_PROMPT = """Keep your answer SHORT (2-3 sentences max). Be helpful and friendly. Use 1-2 emojis. Get straight to the point."""

def create_enhanced_prompt(user_message):
    return f"{SYSTEM_PROMPT}\n\nQuestion: {user_message}\n\nAnswer:"

def process_user_question(question, max_tokens):
    st.session_state.messages.append({"role": "user", "content": question})
    enhanced_prompt = create_enhanced_prompt(question)
    response = generate_response(enhanced_prompt, max_tokens, st.session_state.token)
    response = response.strip()
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar
with st.sidebar:
    # Header
    st.title(" AI Assistant")
    
    st.divider()
    
    # User profile
    st.subheader(" Profile")
    st.success(f"**{st.session_state.username}**")
    st.caption(" Authenticated")
    
    if st.button(" Logout", use_container_width=True, type="secondary"):
        logout()
    
    st.divider()
    
    # Model selection
    st.subheader(" AI Model")
    
    available_models, current_model = get_models(st.session_state.token)
    st.session_state.current_model = current_model
    
    model_descriptions = {
        "mistral": " Fast & Smart",
        "zephyr": " Conversational",
        "llama": " Advanced"
    }
    
    selected_model = st.selectbox(
        "model",
        available_models,
        index=available_models.index(current_model) if current_model in available_models else 0,
        format_func=lambda x: f"{x.title()} {model_descriptions.get(x, '')}",
        label_visibility="collapsed"
    )
    
    if selected_model != st.session_state.current_model:
        with st.spinner("Switching..."):
            result = switch_model(selected_model, st.session_state.token)
            st.success(result)
            st.session_state.current_model = selected_model
            st.rerun()
    
    st.divider()
    
    # Settings
    st.subheader(" Settings")
    
    max_tokens = st.slider(
        "Response Length",
        min_value=50,
        max_value=300,
        value=150,
        step=25,
        help="Adjust response length"
    )
    st.caption(f"**{max_tokens}** tokens (~{max_tokens//2} words)")
    
    st.divider()
    
    # Clear chat
    if st.button(" Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.success("Chat cleared!")
        st.rerun()
    
    st.divider()
    
    # Stats
    st.subheader(" Stats")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(" Total", len(st.session_state.messages))
    with col2:
        st.metric(" Model", st.session_state.current_model.upper()[:3])
    
    st.divider()
    
    # Guide
    with st.expander(" Guide"):
        st.markdown("""
        **Quick Start:**
        1. Type your question
        2. Press Enter
        3. Get AI response
        
        **Tips:**
        - Be specific
        - Try different models
        - Adjust response length
        """)
    
    st.divider()
    
    st.caption("Powered by HuggingFace")
    st.caption("© 2025 AI Assistant")

# Main area
st.title(" AI Chat Assistant")
st.caption(f" Chatting with **{st.session_state.current_model.title()}**")

st.divider()

# Quick actions (when no messages)
if len(st.session_state.messages) == 0:
    st.markdown("###  Quick Actions")
    st.caption("Start with a quick question:")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button(" Tech Fact", use_container_width=True):
            st.session_state.process_question = "Tell me an interesting tech fact"
    
    with col2:
        if st.button(" programming Joke", use_container_width=True):
            st.session_state.process_question = "Tell me a programming joke"
    
    with col3:
        if st.button("  interesting Tip", use_container_width=True):
            st.session_state.process_question = "Give me a coding tip"
    
    with col4:
        if st.button("  AI Concept", use_container_width=True):
            st.session_state.process_question = "Explain an AI concept"
    
    st.info(" **Tip:** Click a button or type your question below!")
    st.divider()

# Process button clicks
if st.session_state.process_question:
    with st.spinner(" Thinking..."):
        process_user_question(st.session_state.process_question, max_tokens)
    st.session_state.process_question = None
    st.rerun()

# Display chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input(" Ask me anything...")

if user_input:
    with st.spinner(" Thinking..."):
        process_user_question(user_input, max_tokens)
    st.rerun()

# Footer
st.divider()
st.caption("Secure Session | Powered by HuggingFace | © 2025 AI Chat Assistant")
