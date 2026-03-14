import sqlite3
import os
from datetime import datetime
import json
import bcrypt
from typing import Optional, List, Dict, Any

class Database:
    def __init__(self, db_path: str = "streetfood.db"):
        self.db_path = db_path
        self.conn = None
        
    def connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def initialize_database(self):
        """Initialize database with schema"""
        with open('database/schema.sql', 'r') as f:
            schema = f.read()
        
        conn = self.connect()
        cursor = conn.cursor()
        cursor.executescript(schema)
        conn.commit()
        
        # Insert default data
        self._insert_default_data()
        print("Database initialized successfully!")
    
    def _insert_default_data(self):
        """Insert default food items and nutrition data"""
        foods_data = [
            {
                'name': 'Samosa',
                'category': 'street_food',
                'meal_type': 'breakfast,snack',
                'region': 'north',
                'is_vegetarian': True,
                'is_vegan': False,
                'is_jain': False,
                'spice_level': 3,
                'description': 'Crispy fried pastry with spiced potato filling',
                'nutrition': {'serving_size': '1 piece', 'serving_size_grams': 50, 'calories': 262, 'protein': 3.5, 'carbohydrates': 24, 'fats': 17.5, 'fiber': 2, 'sugar': 1, 'sodium': 422, 'allergens': ['gluten', 'may contain nuts']}
            },
            {
                'name': 'Vada Pav',
                'category': 'street_food',
                'meal_type': 'breakfast,snack',
                'region': 'mumbai',
                'is_vegetarian': True,
                'is_vegan': False,
                'is_jain': False,
                'spice_level': 4,
                'description': 'Spiced potato fritter in a bun',
                'nutrition': {'serving_size': '1 piece', 'serving_size_grams': 120, 'calories': 286, 'protein': 6, 'carbohydrates': 38, 'fats': 12, 'fiber': 3, 'sugar': 3, 'sodium': 520, 'allergens': ['gluten']}
            },
            {
                'name': 'Pani Puri',
                'category': 'street_food',
                'meal_type': 'snack',
                'region': 'all',
                'is_vegetarian': True,
                'is_vegan': True,
                'is_jain': True,
                'spice_level': 5,
                'description': 'Crispy hollow puri filled with spicy water',
                'nutrition': {'serving_size': '6 pieces', 'serving_size_grams': 90, 'calories': 180, 'protein': 4, 'carbohydrates': 32, 'fats': 4, 'fiber': 2, 'sugar': 5, 'sodium': 380, 'allergens': ['gluten']}
            },
            {
                'name': 'Dhokla',
                'category': 'street_food',
                'meal_type': 'breakfast,snack',
                'region': 'gujarat',
                'is_vegetarian': True,
                'is_vegan': True,
                'is_jain': True,
                'spice_level': 2,
                'description': 'Steamed fermented gram flour cake',
                'nutrition': {'serving_size': '1 piece', 'serving_size_grams': 100, 'calories': 160, 'protein': 5, 'carbohydrates': 28, 'fats': 3, 'fiber': 4, 'sugar': 2, 'sodium': 320, 'allergens': []}
            },
            {
                'name': 'Momos',
                'category': 'street_food',
                'meal_type': 'snack,lunch',
                'region': 'north',
                'is_vegetarian': True,
                'is_vegan': False,
                'is_jain': False,
                'spice_level': 3,
                'description': 'Steamed dumplings with vegetable filling',
                'nutrition': {'serving_size': '6 pieces', 'serving_size_grams': 150, 'calories': 210, 'protein': 7, 'carbohydrates': 35, 'fats': 5, 'fiber': 3, 'sugar': 2, 'sodium': 450, 'allergens': ['gluten', 'soy']}
            },
            {
                'name': 'Pav Bhaji',
                'category': 'street_food',
                'meal_type': 'lunch,dinner',
                'region': 'mumbai',
                'is_vegetarian': True,
                'is_vegan': False,
                'is_jain': False,
                'spice_level': 4,
                'description': 'Spiced mashed vegetables with buttered bread',
                'nutrition': {'serving_size': '1 plate', 'serving_size_grams': 300, 'calories': 450, 'protein': 10, 'carbohydrates': 55, 'fats': 20, 'fiber': 6, 'sugar': 8, 'sodium': 680, 'allergens': ['gluten', 'dairy']}
            },
            {
                'name': 'Idli Sambhar',
                'category': 'main_course',
                'meal_type': 'breakfast',
                'region': 'south',
                'is_vegetarian': True,
                'is_vegan': True,
                'is_jain': False,
                'spice_level': 2,
                'description': 'Steamed rice cakes with lentil soup',
                'nutrition': {'serving_size': '3 idlis with sambhar', 'serving_size_grams': 250, 'calories': 220, 'protein': 8, 'carbohydrates': 42, 'fats': 3, 'fiber': 5, 'sugar': 3, 'sodium': 420, 'allergens': []}
            },
            {
                'name': 'Roti Sabji',
                'category': 'main_course',
                'meal_type': 'lunch,dinner',
                'region': 'all',
                'is_vegetarian': True,
                'is_vegan': False,
                'is_jain': False,
                'spice_level': 3,
                'description': 'Whole wheat flatbread with vegetable curry',
                'nutrition': {'serving_size': '2 rotis with sabji', 'serving_size_grams': 280, 'calories': 320, 'protein': 9, 'carbohydrates': 52, 'fats': 8, 'fiber': 7, 'sugar': 5, 'sodium': 520, 'allergens': ['gluten']}
            },
            {
                'name': 'Dal Rice',
                'category': 'main_course',
                'meal_type': 'lunch,dinner',
                'region': 'all',
                'is_vegetarian': True,
                'is_vegan': True,
                'is_jain': False,
                'spice_level': 2,
                'description': 'Lentil curry with steamed rice',
                'nutrition': {'serving_size': '1 plate', 'serving_size_grams': 350, 'calories': 380, 'protein': 14, 'carbohydrates': 68, 'fats': 5, 'fiber': 8, 'sugar': 2, 'sodium': 480, 'allergens': []}
            },
            {
                'name': 'Bhel Puri',
                'category': 'street_food',
                'meal_type': 'snack',
                'region': 'mumbai',
                'is_vegetarian': True,
                'is_vegan': True,
                'is_jain': True,
                'spice_level': 3,
                'description': 'Puffed rice with vegetables and tangy sauce',
                'nutrition': {'serving_size': '1 plate', 'serving_size_grams': 150, 'calories': 240, 'protein': 5, 'carbohydrates': 42, 'fats': 6, 'fiber': 4, 'sugar': 8, 'sodium': 580, 'allergens': ['peanuts']}
            },
            {
                'name': 'Noodles',
                'category': 'street_food',
                'meal_type': 'lunch,dinner,snack',
                'region': 'all',
                'is_vegetarian': True,
                'is_vegan': False,
                'is_jain': False,
                'spice_level': 3,
                'description': 'Stir-fried noodles with vegetables',
                'nutrition': {'serving_size': '1 plate', 'serving_size_grams': 250, 'calories': 350, 'protein': 8, 'carbohydrates': 58, 'fats': 10, 'fiber': 3, 'sugar': 4, 'sodium': 720, 'allergens': ['gluten', 'soy']}
            }
        ]
        
        cursor = self.conn.cursor()
        
        for food in foods_data:
            # Insert food item
            cursor.execute('''
                INSERT INTO food_items (name, category, meal_type, region, is_vegetarian, 
                                       is_vegan, is_jain, spice_level, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (food['name'], food['category'], food['meal_type'], food['region'],
                  food['is_vegetarian'], food['is_vegan'], food['is_jain'],
                  food['spice_level'], food['description']))
            
            food_id = cursor.lastrowid
            
            # Insert nutrition info
            nutr = food['nutrition']
            cursor.execute('''
                INSERT INTO nutrition_info (food_item_id, serving_size, serving_size_grams,
                                           calories, protein, carbohydrates, fats, fiber,
                                           sugar, sodium, allergens)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (food_id, nutr['serving_size'], nutr['serving_size_grams'],
                  nutr['calories'], nutr['protein'], nutr['carbohydrates'],
                  nutr['fats'], nutr['fiber'], nutr['sugar'], nutr['sodium'],
                  json.dumps(nutr['allergens'])))
        
        # Insert achievements
        achievements = [
            ('First Scan', 'Scanned your first food item', '🎯', json.dumps({'scans': 1}), 10),
            ('Food Explorer', 'Scanned 10 different foods', '🗺️', json.dumps({'unique_foods': 10}), 50),
            ('Healthy Choice', 'Chose healthier alternatives 5 times', '🥗', json.dumps({'healthy_choices': 5}), 30),
            ('Streak Master', 'Logged food for 7 consecutive days', '🔥', json.dumps({'streak_days': 7}), 100),
            ('Nutrition Guru', 'Met daily nutrition goals 10 times', '💪', json.dumps({'goal_days': 10}), 75)
        ]
        
        cursor.executemany('''
            INSERT INTO achievements (name, description, badge_icon, criteria, points)
            VALUES (?, ?, ?, ?, ?)
        ''', achievements)
        
        self.conn.commit()
    
    # User Management
    def create_user(self, username: str, email: str, password: str, full_name: str = None, is_admin: bool = False):
        """Create a new user"""
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, full_name, is_admin)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, email, password_hash, full_name, is_admin))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
    
    def verify_user(self, email: str, password: str):
        """Verify user credentials"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ? AND is_active = 1', (email,))
        user = cursor.fetchone()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return dict(user)
        return None
    
    def get_user_by_id(self, user_id: int):
        """Get user by ID"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        return dict(user) if user else None
    
    # Prediction Management
    def save_prediction(self, user_id: int, food_item_id: int, image_path: str, 
                       predicted_class: str, confidence_score: float, meal_type: str,
                       portion_size: str = 'medium', portion_multiplier: float = 1.0):
        """Save prediction to database"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO predictions (user_id, food_item_id, image_path, predicted_class,
                                    confidence_score, meal_type, portion_size, portion_multiplier)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, food_item_id, image_path, predicted_class, confidence_score,
              meal_type, portion_size, portion_multiplier))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_user_predictions(self, user_id: int, limit: int = 50):
        """Get user's prediction history"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT p.*, f.name as food_name, n.calories, n.protein, n.carbohydrates, n.fats
            FROM predictions p
            LEFT JOIN food_items f ON p.food_item_id = f.id
            LEFT JOIN nutrition_info n ON f.id = n.food_item_id
            WHERE p.user_id = ?
            ORDER BY p.prediction_time DESC
            LIMIT ?
        ''', (user_id, limit))
        return [dict(row) for row in cursor.fetchall()]
    
    # Nutrition & Food Info
    def get_food_by_name(self, name: str):
        """Get food item by name"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT f.*, n.* FROM food_items f
            JOIN nutrition_info n ON f.id = n.food_item_id
            WHERE f.name = ?
        ''', (name,))
        result = cursor.fetchone()
        return dict(result) if result else None
    
    def get_all_foods(self):
        """Get all food items"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT f.*, n.* FROM food_items f
            JOIN nutrition_info n ON f.id = n.food_item_id
        ''')
        return [dict(row) for row in cursor.fetchall()]

if __name__ == "__main__":
    import sys
    db = Database()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--init':
        db.initialize_database()
    else:
        print("Use --init flag to initialize database")
