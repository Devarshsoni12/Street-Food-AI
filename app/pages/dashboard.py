# Dashboard Page
import sys
import os
import streamlit as st
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd
import plotly.express as px
from datetime import datetime
from src.database import Database

# Initialize database
db = Database()
db.connect()

st.title("📊 Nutrition Dashboard")

user_id = st.session_state.user['id']

# Date selector
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    selected_date = st.date_input("📅 Select Date", datetime.now())
with col2:
    view_mode = st.selectbox("📈 View", ["Daily", "Weekly", "Monthly"])
with col3:
    st.metric("🔥 Streak", "3 days")

# Get predictions
predictions = db.get_user_predictions(user_id, limit=100)

# Calculate totals
today_predictions = [p for p in predictions if p['prediction_time'] and p['prediction_time'].startswith(str(selected_date))]

total_calories = sum([p['calories'] or 0 for p in today_predictions])
total_protein = sum([p['protein'] or 0 for p in today_predictions])
total_carbs = sum([p['carbohydrates'] or 0 for p in today_predictions])
total_fats = sum([p['fats'] or 0 for p in today_predictions])

# Daily summary
st.subheader("📋 Today's Summary")
col1, col2, col3, col4 = st.columns(4)

target_calories = 2000
target_protein = 60
target_carbs = 250
target_fats = 65

with col1:
    cal_percent = min(int((total_calories / target_calories) * 100), 100)
    st.metric("Calories", f"{int(total_calories)} / {target_calories}", f"{cal_percent}%")
with col2:
    prot_percent = min(int((total_protein / target_protein) * 100), 100)
    st.metric("Protein", f"{total_protein:.1f}g / {target_protein}g", f"{prot_percent}%")
with col3:
    carb_percent = min(int((total_carbs / target_carbs) * 100), 100)
    st.metric("Carbs", f"{total_carbs:.1f}g / {target_carbs}g", f"{carb_percent}%")
with col4:
    fat_percent = min(int((total_fats / target_fats) * 100), 100)
    st.metric("Fats", f"{total_fats:.1f}g / {target_fats}g", f"{fat_percent}%")

# Progress bars
st.divider()
st.subheader("🎯 Nutrition Goals Progress")

col1, col2 = st.columns(2)

with col1:
    st.write("**Calories**")
    st.progress(cal_percent / 100)
    st.write("**Carbohydrates**")
    st.progress(carb_percent / 100)

with col2:
    st.write("**Protein**")
    st.progress(prot_percent / 100)
    st.write("**Fats**")
    st.progress(fat_percent / 100)

# Recent meals
st.divider()
st.subheader("🍽️ Recent Meals")

if predictions:
    recent_meals = predictions[:10]
    
    meals_data = []
    for p in recent_meals:
        try:
            pred_time = datetime.fromisoformat(p['prediction_time'])
            time_str = pred_time.strftime("%I:%M %p")
        except:
            time_str = "N/A"
        
        meals_data.append({
            'Time': time_str,
            'Food': p['predicted_class'] or 'Unknown',
            'Meal Type': p['meal_type'] or 'Snack',
            'Calories': int(p['calories']) if p['calories'] else 0,
            'Confidence': f"{(p['confidence_score'] or 0) * 100:.1f}%"
        })
    
    df = pd.DataFrame(meals_data)
    st.dataframe(df, width=800, hide_index=True)
else:
    st.info("📭 No meals logged yet. Start by scanning your first food!")
    if st.button("🍛 Scan Food Now"):
        st.session_state.page = 'prediction'
        st.rerun()

# Achievements
st.divider()
st.subheader("🏆 Recent Achievements")

col1, col2, col3 = st.columns(3)

num_predictions = len(predictions)
unique_foods = len(set([p['predicted_class'] for p in predictions if p['predicted_class']]))

with col1:
    if num_predictions >= 1:
        st.success("🎯 First Scan - 10 pts")
    else:
        st.info("🎯 First Scan - Scan your first food!")

with col2:
    if unique_foods >= 5:
        st.success("🗺️ Food Explorer - 50 pts")
    else:
        st.info(f"🗺️ Food Explorer - {unique_foods}/10 foods")

with col3:
    if num_predictions >= 7:
        st.success("🔥 Week Streak - 100 pts")
    else:
        st.info(f"🔥 Week Streak - {num_predictions}/7 days")

db.close()
