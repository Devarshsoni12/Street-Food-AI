import streamlit as st
import sys
import os

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from src.database import Database

# Page configuration
st.set_page_config(
    page_title="Indian Street Food AI",
    page_icon="🍛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #FF6B35;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF6B35;
        color: white;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# Database
try:
    db = Database()
    db.connect()
except Exception as e:
    st.error(f"Database connection error: {e}")
    st.info("Run: python src/database.py --init")
    st.stop()

# Authentication Functions
def show_login():
    st.markdown('<h1 class="main-header">🍛 Indian Street Food AI</h1>', unsafe_allow_html=True)
    st.markdown("### Identify food, track nutrition, stay healthy!")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            st.subheader("Login to Your Account")
            email = st.text_input("Email", placeholder="your@email.com")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                if email and password:
                    user = db.verify_user(email, password)
                    if user:
                        st.session_state.user = user
                        st.session_state.page = 'home'
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
                else:
                    st.warning("Please fill all fields")
    
    with tab2:
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
                    user_id = db.create_user(username, email, password, full_name)
                    if user_id:
                        st.success("Registration successful! Please login.")
                    else:
                        st.error("Username or email already exists")

# Sidebar
def show_sidebar():
    with st.sidebar:
        st.title("🍛 Street Food AI")
        
        if st.session_state.user:
            st.success(f"Welcome, {st.session_state.user['username']}!")
            
            st.subheader("Navigation")
            
            if st.button("🏠 Home", key="nav_home"):
                st.session_state.page = 'home'
                st.rerun()
            
            if st.button("📸 Scan Food", key="nav_scan"):
                st.session_state.page = 'prediction'
                st.rerun()
            
            if st.button("📊 Dashboard", key="nav_dash"):
                st.session_state.page = 'dashboard'
                st.rerun()
            
            if st.button("👤 Profile", key="nav_profile"):
                st.session_state.page = 'profile'
                st.rerun()
            
            if st.session_state.user.get('is_admin'):
                if st.button("⚙️ Admin Panel", key="nav_admin"):
                    st.session_state.page = 'admin'
                    st.rerun()
            
            st.divider()
            
            if st.button("🚪 Logout", key="nav_logout"):
                st.session_state.user = None
                st.session_state.page = 'login'
                st.rerun()
        else:
            st.info("Please login to continue")

# Main App
def main():
    show_sidebar()
    
    if not st.session_state.user:
        show_login()
    else:
        # Import page modules here to avoid circular imports
        page = st.session_state.page
        
        try:
            if page == 'home':
                home_path = os.path.join(current_dir, 'pages', 'home.py')
                exec(open(home_path, encoding='utf-8').read(), {'st': st, '__name__': '__main__', '__file__': home_path})
            elif page == 'prediction':
                pred_path = os.path.join(current_dir, 'pages', 'prediction.py')
                exec(open(pred_path, encoding='utf-8').read(), {'st': st, 'db': db, '__name__': '__main__', '__file__': pred_path})
            elif page == 'dashboard':
                dash_path = os.path.join(current_dir, 'pages', 'dashboard.py')
                exec(open(dash_path, encoding='utf-8').read(), {'st': st, 'db': db, '__name__': '__main__', '__file__': dash_path})
            elif page == 'profile':
                prof_path = os.path.join(current_dir, 'pages', 'profile.py')
                exec(open(prof_path, encoding='utf-8').read(), {'st': st, '__name__': '__main__', '__file__': prof_path})
            elif page == 'admin':
                if st.session_state.user.get('is_admin'):
                    admin_path = os.path.join(current_dir, 'pages', 'admin.py')
                    exec(open(admin_path, encoding='utf-8').read(), {'st': st, 'db': db, '__name__': '__main__', '__file__': admin_path})
                else:
                    st.error("Access Denied. Admin privileges required.")
        except FileNotFoundError as e:
            st.error(f"Page file not found: {e}")
            st.info(f"Looking for: {os.path.join(current_dir, 'pages', page + '.py')}")
        except Exception as e:
            st.error(f"Error loading page: {e}")
            import traceback
            st.code(traceback.format_exc())

if __name__ == "__main__":
    main()
