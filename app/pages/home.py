# Home Page
import streamlit as st
st.markdown('<h1 class="main-header">🍛 Welcome to Indian Street Food AI</h1>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📸 Scan Food")
    st.write("Upload an image and get instant food recognition")
    if st.button("Start Scanning", key="scan_btn"):
        st.session_state.page = 'prediction'
        st.rerun()

with col2:
    st.markdown("### 📊 Track Nutrition")
    st.write("Monitor your daily intake and health goals")
    if st.button("View Dashboard", key="dash_btn"):
        st.session_state.page = 'dashboard'
        st.rerun()

with col3:
    st.markdown("### 🎯 Get Insights")
    st.write("Receive personalized health recommendations")
    if st.button("View Profile", key="prof_btn"):
        st.session_state.page = 'profile'
        st.rerun()

st.divider()

st.subheader("🍕 Supported Foods")
foods = [
    "Aloo Paratha", "Burger", "Chole Bhature", "Dhokla", "Dosa",
    "Grilled Sandwich", "Idli", "Medu Vada", "Misal Pav", "Momos",
    "Pakoda", "Pani Puri", "Pav Bhaji", "Poha", "Samosa",
    "Sev Puri", "Vada Pav"
]

cols = st.columns(4)
for idx, food in enumerate(foods):
    with cols[idx % 4]:
        st.info(f"🍽️ {food}")

st.divider()

st.subheader("✨ Features")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    - 🤖 AI-powered food recognition
    - 📊 Detailed nutrition information
    - 🎯 Personalized health goals
    - 📈 Daily intake tracking
    """)

with col2:
    st.markdown("""
    - 🏆 Achievements & gamification
    - 💡 Smart recommendations
    - ⚠️ Allergen alerts
    - 🌍 Regional variations
    """)
