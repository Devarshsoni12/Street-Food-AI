import streamlit as st
st.title("👤 User Profile")

tab1, tab2, tab3 = st.tabs(["Personal Info", "Health Goals", "Preferences"])

with tab1:
    st.subheader("Personal Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Full Name", value="John Doe")
        st.number_input("Age", min_value=10, max_value=100, value=25)
        st.selectbox("Gender", ["Male", "Female", "Other"])
    
    with col2:
        st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
        st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
        st.metric("BMI", "24.2", "Normal")
    
    if st.button("Update Profile"):
        st.success("Profile updated successfully!")

with tab2:
    st.subheader("Health Goals")
    
    goal = st.selectbox("Primary Goal", [
        "Weight Loss",
        "Weight Gain",
        "Maintenance",
        "Muscle Gain"
    ])
    
    st.number_input("Daily Calorie Target", min_value=1000, max_value=5000, value=2000, step=100)
    
    st.subheader("Macro Targets")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.number_input("Protein (g)", value=60)
    with col2:
        st.number_input("Carbs (g)", value=250)
    with col3:
        st.number_input("Fats (g)", value=65)
    
    if st.button("Save Goals"):
        st.success("Goals saved successfully!")

with tab3:
    st.subheader("Dietary Preferences")
    
    dietary = st.selectbox("Dietary Preference", [
        "No Restriction",
        "Vegetarian",
        "Vegan",
        "Jain"
    ])
    
    st.multiselect("Allergies", [
        "Gluten",
        "Dairy",
        "Nuts",
        "Soy",
        "Eggs"
    ])
    
    st.slider("Spice Tolerance", 1, 5, 3)
    
    st.subheader("Notifications")
    st.checkbox("Daily nutrition reminders", value=True)
    st.checkbox("Achievement notifications", value=True)
    st.checkbox("Health tips", value=True)
    
    if st.button("Save Preferences"):
        st.success("Preferences saved successfully!")
