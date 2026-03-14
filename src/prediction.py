import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple
import json

class PredictionEngine:
    def __init__(self, food_classifier, meal_classifier, database):
        self.food_classifier = food_classifier
        self.meal_classifier = meal_classifier
        self.database = database
    
    def predict_food(self, preprocessed_image, confidence_threshold=0.7):
        """Predict food from image"""
        primary_result, all_results = self.food_classifier.predict_with_threshold(
            preprocessed_image, threshold=confidence_threshold
        )
        return primary_result, all_results
    
    def get_nutrition_info(self, food_name, portion_multiplier=1.0):
        """Get nutrition information for food"""
        food_data = self.database.get_food_by_name(food_name)
        if not food_data:
            return None
        
        nutrition = {
            'serving_size': food_data['serving_size'],
            'calories': round(food_data['calories'] * portion_multiplier, 1),
            'protein': round(food_data['protein'] * portion_multiplier, 1),
            'carbohydrates': round(food_data['carbohydrates'] * portion_multiplier, 1),
            'fats': round(food_data['fats'] * portion_multiplier, 1),
            'fiber': round(food_data['fiber'] * portion_multiplier, 1) if food_data['fiber'] else 0,
            'sugar': round(food_data['sugar'] * portion_multiplier, 1) if food_data['sugar'] else 0,
            'sodium': round(food_data['sodium'] * portion_multiplier, 1) if food_data['sodium'] else 0,
            'allergens': json.loads(food_data['allergens']) if food_data['allergens'] else []
        }
        return nutrition
    
    def get_health_insights(self, nutrition):
        """Generate health insights"""
        insights = []
        if nutrition['calories'] > 400:
            insights.append({'type': 'warning', 'message': f"High calorie content ({nutrition['calories']} kcal)"})
        if nutrition['protein'] > 15:
            insights.append({'type': 'positive', 'message': f"Good protein source ({nutrition['protein']}g)"})
        if nutrition['fats'] > 20:
            insights.append({'type': 'warning', 'message': f"High fat content ({nutrition['fats']}g)"})
        return insights
