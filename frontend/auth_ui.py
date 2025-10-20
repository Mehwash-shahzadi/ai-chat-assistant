import streamlit as st
import requests

API_URL = "http://localhost:8000"

def show_login_page():
    """Display beautiful login page"""
    
    st.markdown("""
        <div style='text-align: center; padding: 50px 0;'>
            <h1>🤖 AI Chat Assistant</h1>
            <p style='font-size: 1.2em; color: #888;'>Please login to continue</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Login")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            
            submit = st.form_submit_button("🚀 Login", use_container_width=True)
            
            if submit:
                if username and password:
                    # Call login API
                    try:
                        response = requests.post(
                            f"{API_URL}/login",
                            json={"username": username, "password": password},
                            timeout=5
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            
                            # Save token and username in session
                            st.session_state.token = data["token"]
                            st.session_state.username = data["username"]
                            st.session_state.authenticated = True
                            
                            st.success("✅ Login successful!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid username or password")
                    
                    except requests.exceptions.ConnectionError:
                        st.error("⚠️ Cannot connect to backend. Make sure it's running!")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                else:
                    st.warning("⚠️ Please enter both username and password")
        
        # Demo credentials
        with st.expander("💡 Demo Accounts"):
            st.markdown("""
            **Test accounts:**
            - Username: `demo` | Password: `demo123`
            - Username: `admin` | Password: `admin123`
            - Username: `user` | Password: `password`
            """)
        
        # Info section
        st.info("🔒 Your credentials are securely hashed and stored.")

def logout():
    """Logout user"""
    try:
        if "token" in st.session_state:
            # Call logout API
            requests.post(
                f"{API_URL}/logout",
                params={"token": st.session_state.token}
            )
    except:
        pass
    
    # Clear session
    st.session_state.authenticated = False
    st.session_state.token = None
    st.session_state.username = None
    st.session_state.messages = []
    st.rerun()