import streamlit as st
import requests

API_URL = "http://localhost:8000"

def show_login_page():
    """Display professional login page - NO demo credentials shown"""
    
    # Clean header
    st.markdown("""
        <div style='text-align: center; padding: 30px 0 20px 0;'>
            <h1 style='font-size: 3em; margin-bottom: 10px;'>🤖</h1>
            <h2 style='margin-top: 0;'>AI Chat Assistant</h2>
            <p style='font-size: 1.1em; color: #666; margin-top: 10px;'>
                Secure Authentication Required
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Centered login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Login card style
        with st.container():
            st.markdown("###  Sign In")
            
            with st.form("login_form", clear_on_submit=True):
                username = st.text_input(
                    "Username",
                    placeholder="Enter your username",
                    help="Your registered username",
                    key="login_username"
                )

                # Ensure show_password state exists and use it consistently
                if "show_password" not in st.session_state:
                    st.session_state.show_password = False

                show_password = st.checkbox(
                    "Show password",
                    value=st.session_state.show_password,
                    help="Toggle to show/hide password",
                    key="show_password"
                )

                # Use explicit input_type derived from the checkbox state.
                input_type = "text" if st.session_state.show_password else "password"

                password = st.text_input(
                    "Password",
                    type=input_type,
                    placeholder="Enter your password",
                    help="Your secure password",
                    key="password_input"
                )
                
                # Remember me option
                remember = st.checkbox("Remember me for 24 hours", key="remember_me")
                
                submit = st.form_submit_button(
                    " Sign In",
                    use_container_width=True,
                    type="primary"
                )
                
                if submit:
                    if username and password:
                        with st.spinner(" Authenticating..."):
                            try:
                                response = requests.post(
                                    f"{API_URL}/login",
                                    json={
                                        "username": username,
                                        "password": password
                                    },
                                    timeout=5
                                )
                                
                                if response.status_code == 200:
                                    data = response.json()
                                    
                                    # Save to session
                                    st.session_state.token = data["token"]
                                    st.session_state.username = data["username"]
                                    st.session_state.authenticated = True
                                    
                                    st.success(f" Welcome back, {data['username']}!")
                                    st.balloons()
                                    st.rerun()
                                    
                                elif response.status_code == 401:
                                    st.error(" Invalid username or password")
                                else:
                                    st.error(" Login failed. Please try again.")
                            
                            except requests.exceptions.ConnectionError:
                                st.error(" **Backend not running!**")
                                st.info("Start backend: `uvicorn backend.main:app --reload`")
                            except requests.exceptions.Timeout:
                                st.error(" Request timed out. Please try again.")
                            except Exception as e:
                                st.error(f" Error: {str(e)}")
                    else:
                        st.warning(" Please enter both username and password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Security info
            with st.expander(" Security Information"):
                st.markdown("""
                **Your security is our priority:**
                
                  Passwords encrypted with **bcrypt**
                
                  Secure session tokens
                
                  24-hour automatic logout
                
                  No password storage in plaintext
                
                  Industry-standard security practices
                """)
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center; color: #666; font-size: 0.9em;'>
            <p> Protected by bcrypt encryption | © 2025 AI Chat Assistant</p>
        </div>
    """, unsafe_allow_html=True)

def logout():
    """Logout user - Clean session"""
    try:
        if "token" in st.session_state and st.session_state.token:
            # Call logout API
            requests.post(
                f"{API_URL}/logout",
                params={"token": st.session_state.token},
                timeout=3
            )
    except:
        pass
    
    # Clear all session data
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    st.success(" Logged out successfully")
    st.rerun()
