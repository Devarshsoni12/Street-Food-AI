# Prediction Page
import sys
import streamlit as st
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from PIL import Image
import numpy as np
import random
from datetime import datetime
import json
from src.database import Database

# Initialize database
db = Database()
db.connect()

CLASS_NAMES = [
    'Aloo Paratha', 'Burger', 'Chole Bhature', 'Dhokla', 'Dosa',
    'Grilled Sandwich', 'Idli', 'Medul Vada', 'Misal Pav', 'Momos',
    'Pakoda', 'Pani Puri', 'Pav Bhaji', 'Poha', 'Samosa',
    'Sev Puri', 'Vada Pav'
]

MODEL_PATH = 'models/food_classifier.h5'

# Load model if exists
@st.cache_resource
def load_model():
    if os.path.exists(MODEL_PATH):
        import tensorflow as tf
        model = tf.keras.models.load_model(MODEL_PATH)
        return model
    return None

model = load_model()

def predict_food(image):
    if model is None:
        # No model - return random
        food_name = random.choice(CLASS_NAMES)
        confidence = random.uniform(0.60, 0.85)
        return food_name, confidence, False
    else:
        # Real model prediction
        img = image.resize((224, 224))
        img_array = np.array(img.convert('RGB')) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        predictions = model.predict(img_array, verbose=0)
        idx = np.argmax(predictions[0])
        confidence = float(predictions[0][idx])
        return CLASS_NAMES[idx], confidence, True

st.title("Food Recognition & Nutrition Analysis")

# Get all foods
all_foods = db.get_all_foods()
food_name_map = {f['name']: f for f in all_foods}

if model:
    st.success("AI Model loaded! Real predictions active.")
else:
    st.warning("No trained model found. Showing random predictions. Run train_model.py to train.")

st.info("Upload an image of Indian street food to get instant recognition and nutrition info!")

uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Uploaded Image")
        st.image(image, width=400)

        st.subheader("Portion Size")
        portion = st.select_slider(
            "Select portion size:",
            options=["Small", "Medium", "Large", "Extra Large"],
            value="Medium"
        )

        portion_multipliers = {
            "Small": 0.7,
            "Medium": 1.0,
            "Large": 1.3,
            "Extra Large": 1.6
        }
        multiplier = portion_multipliers[portion]

    with col2:
        st.subheader("Prediction Results")

        with st.spinner("Analyzing image..."):
            import time
            time.sleep(0.5)

            predicted_food, confidence, is_real = predict_food(image)

            # Determine meal type
            hour = datetime.now().hour
            if 5 <= hour < 11:
                meal_type = "Breakfast"
            elif 11 <= hour < 16:
                meal_type = "Lunch"
            elif 16 <= hour < 22:
                meal_type = "Dinner"
            else:
                meal_type = "Snack"

            if is_real:
                st.success(f"Detected: {predicted_food}")
            else:
                st.warning("Random prediction (no model trained yet)")
                st.info(f"Predicted: {predicted_food}")

            col_a, col_b = st.columns(2)
            col_a.metric("Confidence", f"{confidence*100:.1f}%")
            col_b.metric("Meal Type", meal_type)

            # Get nutrition from database
            food = food_name_map.get(predicted_food)

            if food:
                st.divider()
                st.subheader("Nutrition Information")
                st.caption(f"Per serving: {food['serving_size']} ({portion} portion)")

                col_a, col_b, col_c, col_d = st.columns(4)
                col_a.metric("Calories", f"{int(food['calories'] * multiplier)} kcal")
                col_b.metric("Protein", f"{food['protein'] * multiplier:.1f}g")
                col_c.metric("Carbs", f"{food['carbohydrates'] * multiplier:.1f}g")
                col_d.metric("Fats", f"{food['fats'] * multiplier:.1f}g")

                # Health Insights
                st.divider()
                st.subheader("Health Insights")
                calories = food['calories'] * multiplier
                if calories > 400:
                    st.warning(f"High calorie content ({int(calories)} kcal)")
                else:
                    st.success(f"Moderate calorie content ({int(calories)} kcal)")

                allergens = json.loads(food['allergens']) if food['allergens'] else []
                if allergens:
                    st.error(f"Allergen Alert: Contains {', '.join(allergens)}")

                st.divider()
                st.subheader("Dietary Information")
                col1, col2, col3, col4 = st.columns(4)
                col1.write("Vegetarian" if food['is_vegetarian'] else "Non-Veg")
                col2.write("Vegan" if food['is_vegan'] else "Not Vegan")
                col3.write("Jain" if food['is_jain'] else "Not Jain")
                col4.write(f"Spice: {food['spice_level']}/5")

                st.divider()
                if st.button("Save to Food Diary", type="primary"):
                    user_id = st.session_state.user['id']
                    db.save_prediction(
                        user_id=user_id,
                        food_item_id=food['id'],
                        image_path=f"uploads/{user_id}/{uploaded_file.name}",
                        predicted_class=predicted_food,
                        confidence_score=confidence,
                        meal_type=meal_type,
                        portion_size=portion,
                        portion_multiplier=multiplier
                    )
                    st.success("Saved to your food diary!")
                    st.balloons()
            else:
                st.info(f"Nutrition data for '{predicted_food}' not in database yet.")

else:
    st.info("Upload an image to get started")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Tips for Best Results")
        st.write("Use clear, well-lit images")
        st.write("Capture the food from above")
        st.write("Ensure the food is the main focus")
        st.write("Avoid blurry or dark images")

    with col2:
        st.subheader("Supported Foods")
        for name in CLASS_NAMES:
            st.write(f"- {name}")

db.close()
