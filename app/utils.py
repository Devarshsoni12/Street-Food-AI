import os
import hashlib
from datetime import datetime
import json

def save_uploaded_file(uploaded_file, user_id):
    """Save uploaded file and return path"""
    upload_dir = f"data/uploads/{user_id}"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_ext = uploaded_file.name.split('.')[-1]
    filename = f"{timestamp}.{file_ext}"
    
    filepath = os.path.join(upload_dir, filename)
    
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return filepath

def format_nutrition_display(nutrition):
    """Format nutrition data for display"""
    return {
        'Calories': f"{nutrition['calories']} kcal",
        'Protein': f"{nutrition['protein']}g",
        'Carbohydrates': f"{nutrition['carbohydrates']}g",
        'Fats': f"{nutrition['fats']}g",
        'Fiber': f"{nutrition['fiber']}g",
        'Sugar': f"{nutrition['sugar']}g",
        'Sodium': f"{nutrition['sodium']}mg"
    }

def calculate_streak(user_predictions):
    """Calculate user's streak of consecutive days"""
    if not user_predictions:
        return 0
    
    dates = sorted(set([p['prediction_time'].date() for p in user_predictions]), reverse=True)
    
    streak = 1
    for i in range(len(dates) - 1):
        diff = (dates[i] - dates[i + 1]).days
        if diff == 1:
            streak += 1
        else:
            break
    
    return streak

def check_achievements(user_id, database):
    """Check and award achievements"""
    predictions = database.get_user_predictions(user_id)
    
    achievements_earned = []
    
    # First scan
    if len(predictions) == 1:
        achievements_earned.append('First Scan')
    
    # Food explorer (10 unique foods)
    unique_foods = len(set([p['predicted_class'] for p in predictions]))
    if unique_foods >= 10:
        achievements_earned.append('Food Explorer')
    
    # Streak master
    streak = calculate_streak(predictions)
    if streak >= 7:
        achievements_earned.append('Streak Master')
    
    return achievements_earned

def get_portion_multiplier(portion_size):
    """Get multiplier based on portion size"""
    multipliers = {
        'small': 0.7,
        'medium': 1.0,
        'large': 1.3,
        'extra_large': 1.6
    }
    return multipliers.get(portion_size, 1.0)
