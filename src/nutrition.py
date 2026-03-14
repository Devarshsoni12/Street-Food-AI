import json
from typing import Dict, List

class NutritionAnalyzer:
    def __init__(self, database):
        self.database = database
    
    def calculate_daily_intake(self, user_id, date):
        """Calculate total daily nutrition intake"""
        cursor = self.database.conn.cursor()
        cursor.execute('''
            SELECT SUM(calories) as total_calories,
                   SUM(protein) as total_protein,
                   SUM(carbohydrates) as total_carbs,
                   SUM(fats) as total_fats
            FROM daily_intake
            WHERE user_id = ? AND date = ?
        ''', (user_id, date))
        
        result = cursor.fetchone()
        return dict(result) if result else None
    
    def check_dietary_restrictions(self, food_data, user_profile):
        """Check if food matches user dietary restrictions"""
        alerts = []
        
        if user_profile.get('dietary_preference') == 'vegan' and not food_data['is_vegan']:
            alerts.append("This food is not vegan")
        
        if user_profile.get('dietary_preference') == 'jain' and not food_data['is_jain']:
            alerts.append("This food is not Jain-friendly")
        
        user_allergies = json.loads(user_profile.get('allergies', '[]'))
        food_allergens = json.loads(food_data.get('allergens', '[]'))
        
        common_allergens = set(user_allergies) & set(food_allergens)
        if common_allergens:
            alerts.append(f"Contains allergens: {', '.join(common_allergens)}")
        
        return alerts
    
    def calculate_bmi(self, weight_kg, height_cm):
        """Calculate BMI"""
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        return round(bmi, 1)
    
    def get_calorie_recommendation(self, user_profile):
        """Get daily calorie recommendation"""
        age = user_profile.get('age', 30)
        weight = user_profile.get('weight', 70)
        height = user_profile.get('height', 170)
        gender = user_profile.get('gender', 'male')
        goal = user_profile.get('health_goal', 'maintenance')
        
        # Mifflin-St Jeor Equation
        if gender == 'male':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        
        # Activity multiplier (assuming moderate activity)
        tdee = bmr * 1.55
        
        # Adjust based on goal
        if goal == 'weight_loss':
            target = tdee - 500
        elif goal == 'weight_gain':
            target = tdee + 500
        else:
            target = tdee
        
        return round(target)
