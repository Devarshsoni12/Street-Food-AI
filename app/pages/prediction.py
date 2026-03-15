# Prediction Page
import sys
import streamlit as st
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from PIL import Image
import numpy as np
from datetime import datetime
import json

# db is injected via exec() from streamlit_app.py; fallback for standalone run
if 'db' not in dir():
    from src.database import Database
    db = Database()
    db.connect()

_CLASS_INDICES_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    'models', 'class_indices.json'
)

# Load class names in the exact order the model was trained with
if os.path.exists(_CLASS_INDICES_PATH):
    with open(_CLASS_INDICES_PATH, 'r') as _f:
        _indices = json.load(_f)
    # Sort by index value to get ordered list, then replace underscores with spaces
    CLASS_NAMES = [k.replace('_', ' ') for k, v in sorted(_indices.items(), key=lambda x: x[1])]
else:
    # Fallback — order must match class_indices.json exactly
    CLASS_NAMES = [
        'Aloo Paratha', 'Burger', 'Chole Bhature', 'Dhokla', 'Dosa',
        'Grilled Sandwich', 'Idli', 'Medu Vada', 'Misal Pav', 'Momos',
        'Pakoda', 'Pani Puri', 'Pav Bhaji', 'Poha', 'Samosa',
        'Sev Puri', 'Unknown', 'Vada Pav'
    ]

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    'models', 'food_classifier.h5'
)

@st.cache_resource
def load_model():
    if os.path.exists(MODEL_PATH):
        import tensorflow as tf
        return tf.keras.models.load_model(MODEL_PATH)
    return None

model = load_model()

def predict_food(image):
    """Returns (food_name, confidence, used_real_model)"""
    if model is None:
        return None, 0.0, False

    img = image.resize((224, 224))
    img_array = np.array(img.convert('RGB')) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    predictions = model.predict(img_array, verbose=0)
    idx = int(np.argmax(predictions[0]))
    confidence = float(predictions[0][idx])
    food_name = CLASS_NAMES[idx]

    # Reject if Unknown class or confidence below threshold
    if food_name == 'Unknown' or confidence < 0.75:
        return 'Unknown', confidence, True

    return food_name, confidence, True

# ── UI ────────────────────────────────────────────────────────────────────────
st.title("Food Recognition & Nutrition Analysis")

# Build food lookup from db passed via exec context
all_foods = db.get_all_foods()
# Normalize keys: lowercase stripped for robust matching
food_name_map = {}
for f in all_foods:
    food_name_map[f['name'].strip()] = f
    food_name_map[f['name'].strip().lower()] = f

def lookup_food(name):
    return food_name_map.get(name.strip()) or food_name_map.get(name.strip().lower())

if model:
    st.success("AI Model loaded! Real predictions active.")
else:
    st.warning("No trained model found. Run `python train_model.py` to train the model first.")

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
        portion_multipliers = {"Small": 0.7, "Medium": 1.0, "Large": 1.3, "Extra Large": 1.6}
        multiplier = portion_multipliers[portion]

    with col2:
        st.subheader("Prediction Results")

        with st.spinner("Analyzing image..."):
            import time
            time.sleep(0.5)

            predicted_food, confidence, used_model = predict_food(image)

            hour = datetime.now().hour
            if 5 <= hour < 11:
                meal_type = "Breakfast"
            elif 11 <= hour < 16:
                meal_type = "Lunch"
            elif 16 <= hour < 22:
                meal_type = "Dinner"
            else:
                meal_type = "Snack"

            if not used_model:
                st.error("No trained model found. Please train the model first by running `python train_model.py`.")
                st.stop()

            if predicted_food == 'Unknown':
                st.error("This image is not a recognized Indian street food!")
                st.warning(f"Confidence was too low ({confidence*100:.1f}%) or the food is not in our database.")
                st.info("Please upload a clear image of one of the supported Indian street food items.")
                st.stop()

            st.success(f"Detected: {predicted_food}")
            col_a, col_b = st.columns(2)
            col_a.metric("Confidence", f"{confidence*100:.1f}%")
            col_b.metric("Meal Type", meal_type)

            # Nutrition lookup
            food = lookup_food(predicted_food)

            if food:
                st.divider()
                st.subheader("Nutrition Information")
                st.caption(f"Per serving: {food['serving_size']} ({portion} portion)")

                col_a, col_b, col_c, col_d = st.columns(4)
                col_a.metric("Calories", f"{int(food['calories'] * multiplier)} kcal")
                col_b.metric("Protein", f"{food['protein'] * multiplier:.1f}g")
                col_c.metric("Carbs", f"{food['carbohydrates'] * multiplier:.1f}g")
                col_d.metric("Fats", f"{food['fats'] * multiplier:.1f}g")

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
                c1, c2, c3, c4 = st.columns(4)
                c1.write("Vegetarian" if food['is_vegetarian'] else "Non-Veg")
                c2.write("Vegan" if food['is_vegan'] else "Not Vegan")
                c3.write("Jain" if food['is_jain'] else "Not Jain")
                c4.write(f"Spice: {food['spice_level']}/5")

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
                st.warning(f"Nutrition data for '{predicted_food}' not found in database.")
                st.info("Run `python database/seed_data.py` to populate nutrition data.")

else:
    st.info("Upload an image to get started")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Tips for Best Results")
        st.write("- Use clear, well-lit images")
        st.write("- Capture the food from above or at an angle")
        st.write("- Ensure the food is the main focus")
        st.write("- Avoid blurry or dark images")

    with col2:
        st.subheader("Supported Foods")
        for name in CLASS_NAMES[:-1]:  # exclude Unknown
            st.write(f"- {name}")
