import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import Database

class AuthManager:
    def __init__(self):
        self.db = Database()
        self.db.connect()
    
    def show_auth_page(self):
        """Display login/register page"""
        st.markdown('<h1 class="main-header">🍛 Indian Street Food AI</h1>', unsafe_allow_html=True)
        st.markdown("### Identify food, track nutrition, stay healthy!")
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            self.show_login_form()
        
        with tab2:
            self.show_register_form()
    
    def show_login_form(self):
        """Display login form"""
        with st.form("login_form"):
            st.subheader("Login to Your Account")
            email = st.text_input("Email", placeholder="your@email.com")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                if email and password:
                    user = self.db.verify_user(email, password)
                    if user:
                        st.session_state.user = user
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
                else:
                    st.warning("Please fill all fields")
    
    def show_register_form(self):
        """Display registration form"""
        with st.form("register_form"):
            st.subheader("Create New Account")
            username = st.text_input("Username")
            email = st.text_input("Email")
            full_name = st.text_input("Full Name")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("Register")
            
            if submit:
                if not all([username, email, password, confirm_password]):
                    st.warning("Please fill all fields")
                elif password != confirm_password:
                    st.error("Passwords don't match")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    user_id = self.db.create_user(username, email, password, full_name)
                    if user_id:
                        st.success("Registration successful! Please login.")
                    else:
                        st.error("Username or email already exists")
