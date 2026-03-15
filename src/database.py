import os
import json
import bcrypt
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./streetfood.db")

# Detect which backend to use
USE_POSTGRES = DATABASE_URL.startswith("postgresql") or DATABASE_URL.startswith("postgres")

if USE_POSTGRES:
    try:
        import psycopg2
        import psycopg2.extras
    except ImportError:
        raise ImportError("psycopg2 not installed. Run: pip install psycopg2-binary")
else:
    import sqlite3


class Database:
    def __init__(self):
        self.conn = None

    def connect(self):
        """Establish database connection (SQLite or PostgreSQL)"""
        if USE_POSTGRES:
            try:
                self.conn = psycopg2.connect(DATABASE_URL)
                self.conn.autocommit = False
            except Exception as e:
                raise ConnectionError(f"Failed to connect to PostgreSQL: {e}")
        else:
            # Extract file path from sqlite:///./path or use default
            db_path = DATABASE_URL.replace("sqlite:///", "").replace("sqlite://", "")
            if db_path.startswith("./"):
                db_path = db_path[2:]
            self.conn = sqlite3.connect(db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
        return self.conn

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def _cursor(self, dict_cursor=False):
        """Return appropriate cursor"""
        if USE_POSTGRES:
            if dict_cursor:
                return self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            return self.conn.cursor()
        else:
            return self.conn.cursor()

    def _ph(self):
        """Return correct placeholder: %s for postgres, ? for sqlite"""
        return "%s" if USE_POSTGRES else "?"

    def _commit(self):
        self.conn.commit()

    def _fetchrow(self, cursor):
        """Fetch one row as dict"""
        row = cursor.fetchone()
        if row is None:
            return None
        return dict(row)

    def _fetchall(self, cursor):
        """Fetch all rows as list of dicts"""
        return [dict(row) for row in cursor.fetchall()]

    def initialize_database(self):
        """Initialize database with schema"""
        schema_file = 'database/schema.sql' if USE_POSTGRES else 'database/schema_sqlite.sql'
        with open(schema_file, 'r') as f:
            schema = f.read()

        cursor = self._cursor()
        if USE_POSTGRES:
            cursor.execute(schema)
        else:
            cursor.executescript(schema)
        self._commit()
        self._insert_default_data()
        print("Database initialized successfully!")

    def _insert_default_data(self):
        """Insert default food items and nutrition data"""
        ph = self._ph()
        foods_data = [
            {
                'name': 'Samosa', 'category': 'street_food', 'meal_type': 'breakfast,snack',
                'region': 'north', 'is_vegetarian': True, 'is_vegan': False, 'is_jain': False,
                'spice_level': 3, 'description': 'Crispy fried pastry with spiced potato filling',
                'nutrition': {'serving_size': '1 piece', 'serving_size_grams': 50, 'calories': 262,
                              'protein': 3.5, 'carbohydrates': 24, 'fats': 17.5, 'fiber': 2,
                              'sugar': 1, 'sodium': 422, 'allergens': ['gluten', 'may contain nuts']}
            },
            {
                'name': 'Vada Pav', 'category': 'street_food', 'meal_type': 'breakfast,snack',
                'region': 'mumbai', 'is_vegetarian': True, 'is_vegan': False, 'is_jain': False,
                'spice_level': 4, 'description': 'Spiced potato fritter in a bun',
                'nutrition': {'serving_size': '1 piece', 'serving_size_grams': 120, 'calories': 286,
                              'protein': 6, 'carbohydrates': 38, 'fats': 12, 'fiber': 3,
                              'sugar': 3, 'sodium': 520, 'allergens': ['gluten']}
            },
            {
                'name': 'Pani Puri', 'category': 'street_food', 'meal_type': 'snack',
                'region': 'all', 'is_vegetarian': True, 'is_vegan': True, 'is_jain': True,
                'spice_level': 5, 'description': 'Crispy hollow puri filled with spicy water',
                'nutrition': {'serving_size': '6 pieces', 'serving_size_grams': 90, 'calories': 180,
                              'protein': 4, 'carbohydrates': 32, 'fats': 4, 'fiber': 2,
                              'sugar': 5, 'sodium': 380, 'allergens': ['gluten']}
            },
            {
                'name': 'Dhokla', 'category': 'street_food', 'meal_type': 'breakfast,snack',
                'region': 'gujarat', 'is_vegetarian': True, 'is_vegan': True, 'is_jain': True,
                'spice_level': 2, 'description': 'Steamed fermented gram flour cake',
                'nutrition': {'serving_size': '1 piece', 'serving_size_grams': 100, 'calories': 160,
                              'protein': 5, 'carbohydrates': 28, 'fats': 3, 'fiber': 4,
                              'sugar': 2, 'sodium': 320, 'allergens': []}
            },
            {
                'name': 'Momos', 'category': 'street_food', 'meal_type': 'snack,lunch',
                'region': 'north', 'is_vegetarian': True, 'is_vegan': False, 'is_jain': False,
                'spice_level': 3, 'description': 'Steamed dumplings with vegetable filling',
                'nutrition': {'serving_size': '6 pieces', 'serving_size_grams': 150, 'calories': 210,
                              'protein': 7, 'carbohydrates': 35, 'fats': 5, 'fiber': 3,
                              'sugar': 2, 'sodium': 450, 'allergens': ['gluten', 'soy']}
            },
            {
                'name': 'Pav Bhaji', 'category': 'street_food', 'meal_type': 'lunch,dinner',
                'region': 'mumbai', 'is_vegetarian': True, 'is_vegan': False, 'is_jain': False,
                'spice_level': 4, 'description': 'Spiced mashed vegetables with buttered bread',
                'nutrition': {'serving_size': '1 plate', 'serving_size_grams': 300, 'calories': 450,
                              'protein': 10, 'carbohydrates': 55, 'fats': 20, 'fiber': 6,
                              'sugar': 8, 'sodium': 680, 'allergens': ['gluten', 'dairy']}
            },
            {
                'name': 'Idli Sambhar', 'category': 'main_course', 'meal_type': 'breakfast',
                'region': 'south', 'is_vegetarian': True, 'is_vegan': True, 'is_jain': False,
                'spice_level': 2, 'description': 'Steamed rice cakes with lentil soup',
                'nutrition': {'serving_size': '3 idlis with sambhar', 'serving_size_grams': 250,
                              'calories': 220, 'protein': 8, 'carbohydrates': 42, 'fats': 3,
                              'fiber': 5, 'sugar': 3, 'sodium': 420, 'allergens': []}
            },
            {
                'name': 'Roti Sabji', 'category': 'main_course', 'meal_type': 'lunch,dinner',
                'region': 'all', 'is_vegetarian': True, 'is_vegan': False, 'is_jain': False,
                'spice_level': 3, 'description': 'Whole wheat flatbread with vegetable curry',
                'nutrition': {'serving_size': '2 rotis with sabji', 'serving_size_grams': 280,
                              'calories': 320, 'protein': 9, 'carbohydrates': 52, 'fats': 8,
                              'fiber': 7, 'sugar': 5, 'sodium': 520, 'allergens': ['gluten']}
            },
            {
                'name': 'Dal Rice', 'category': 'main_course', 'meal_type': 'lunch,dinner',
                'region': 'all', 'is_vegetarian': True, 'is_vegan': True, 'is_jain': False,
                'spice_level': 2, 'description': 'Lentil curry with steamed rice',
                'nutrition': {'serving_size': '1 plate', 'serving_size_grams': 350, 'calories': 380,
                              'protein': 14, 'carbohydrates': 68, 'fats': 5, 'fiber': 8,
                              'sugar': 2, 'sodium': 480, 'allergens': []}
            },
            {
                'name': 'Bhel Puri', 'category': 'street_food', 'meal_type': 'snack',
                'region': 'mumbai', 'is_vegetarian': True, 'is_vegan': True, 'is_jain': True,
                'spice_level': 3, 'description': 'Puffed rice with vegetables and tangy sauce',
                'nutrition': {'serving_size': '1 plate', 'serving_size_grams': 150, 'calories': 240,
                              'protein': 5, 'carbohydrates': 42, 'fats': 6, 'fiber': 4,
                              'sugar': 8, 'sodium': 580, 'allergens': ['peanuts']}
            },
            {
                'name': 'Noodles', 'category': 'street_food', 'meal_type': 'lunch,dinner,snack',
                'region': 'all', 'is_vegetarian': True, 'is_vegan': False, 'is_jain': False,
                'spice_level': 3, 'description': 'Stir-fried noodles with vegetables',
                'nutrition': {'serving_size': '1 plate', 'serving_size_grams': 250, 'calories': 350,
                              'protein': 8, 'carbohydrates': 58, 'fats': 10, 'fiber': 3,
                              'sugar': 4, 'sodium': 720, 'allergens': ['gluten', 'soy']}
            }
        ]

        cursor = self._cursor()
        for food in foods_data:
            if USE_POSTGRES:
                cursor.execute(f'''
                    INSERT INTO food_items (name, category, meal_type, region, is_vegetarian,
                                           is_vegan, is_jain, spice_level, description)
                    VALUES ({ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph}) RETURNING id
                ''', (food['name'], food['category'], food['meal_type'], food['region'],
                      food['is_vegetarian'], food['is_vegan'], food['is_jain'],
                      food['spice_level'], food['description']))
                food_id = cursor.fetchone()[0]
            else:
                cursor.execute(f'''
                    INSERT INTO food_items (name, category, meal_type, region, is_vegetarian,
                                           is_vegan, is_jain, spice_level, description)
                    VALUES ({ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph})
                ''', (food['name'], food['category'], food['meal_type'], food['region'],
                      food['is_vegetarian'], food['is_vegan'], food['is_jain'],
                      food['spice_level'], food['description']))
                food_id = cursor.lastrowid

            nutr = food['nutrition']
            cursor.execute(f'''
                INSERT INTO nutrition_info (food_item_id, serving_size, serving_size_grams,
                                           calories, protein, carbohydrates, fats, fiber,
                                           sugar, sodium, allergens)
                VALUES ({ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph})
            ''', (food_id, nutr['serving_size'], nutr['serving_size_grams'],
                  nutr['calories'], nutr['protein'], nutr['carbohydrates'],
                  nutr['fats'], nutr['fiber'], nutr['sugar'], nutr['sodium'],
                  json.dumps(nutr['allergens'])))

        achievements = [
            ('First Scan', 'Scanned your first food item', '🎯', json.dumps({'scans': 1}), 10),
            ('Food Explorer', 'Scanned 10 different foods', '🗺️', json.dumps({'unique_foods': 10}), 50),
            ('Healthy Choice', 'Chose healthier alternatives 5 times', '🥗', json.dumps({'healthy_choices': 5}), 30),
            ('Streak Master', 'Logged food for 7 consecutive days', '🔥', json.dumps({'streak_days': 7}), 100),
            ('Nutrition Guru', 'Met daily nutrition goals 10 times', '💪', json.dumps({'goal_days': 10}), 75)
        ]
        cursor.executemany(f'''
            INSERT INTO achievements (name, description, badge_icon, criteria, points)
            VALUES ({ph},{ph},{ph},{ph},{ph})
        ''', achievements)
        self._commit()

    # User Management
    def create_user(self, username: str, email: str, password: str, full_name: str = None, is_admin: bool = False):
        """Create a new user"""
        ph = self._ph()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor = self._cursor()
        try:
            if USE_POSTGRES:
                cursor.execute(f'''
                    INSERT INTO users (username, email, password_hash, full_name, is_admin)
                    VALUES ({ph},{ph},{ph},{ph},{ph}) RETURNING id
                ''', (username, email, password_hash, full_name, is_admin))
                user_id = cursor.fetchone()[0]
            else:
                cursor.execute(f'''
                    INSERT INTO users (username, email, password_hash, full_name, is_admin)
                    VALUES ({ph},{ph},{ph},{ph},{ph})
                ''', (username, email, password_hash, full_name, is_admin))
                user_id = cursor.lastrowid
            self._commit()
            return user_id
        except Exception:
            if USE_POSTGRES:
                self.conn.rollback()
            return None

    def verify_user(self, email: str, password: str):
        """Verify user credentials"""
        ph = self._ph()
        cursor = self._cursor(dict_cursor=True)
        cursor.execute(f'SELECT * FROM users WHERE email = {ph} AND is_active = 1', (email,))
        user = self._fetchrow(cursor)
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return user
        return None

    def get_user_by_id(self, user_id: int):
        """Get user by ID"""
        ph = self._ph()
        cursor = self._cursor(dict_cursor=True)
        cursor.execute(f'SELECT * FROM users WHERE id = {ph}', (user_id,))
        return self._fetchrow(cursor)

    # Prediction Management
    def save_prediction(self, user_id: int, food_item_id: int, image_path: str,
                        predicted_class: str, confidence_score: float, meal_type: str,
                        portion_size: str = 'medium', portion_multiplier: float = 1.0):
        """Save prediction to database"""
        ph = self._ph()
        cursor = self._cursor()
        if USE_POSTGRES:
            cursor.execute(f'''
                INSERT INTO predictions (user_id, food_item_id, image_path, predicted_class,
                                        confidence_score, meal_type, portion_size, portion_multiplier)
                VALUES ({ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph}) RETURNING id
            ''', (user_id, food_item_id, image_path, predicted_class,
                  confidence_score, meal_type, portion_size, portion_multiplier))
            pred_id = cursor.fetchone()[0]
        else:
            cursor.execute(f'''
                INSERT INTO predictions (user_id, food_item_id, image_path, predicted_class,
                                        confidence_score, meal_type, portion_size, portion_multiplier)
                VALUES ({ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph})
            ''', (user_id, food_item_id, image_path, predicted_class,
                  confidence_score, meal_type, portion_size, portion_multiplier))
            pred_id = cursor.lastrowid
        self._commit()
        return pred_id

    def get_user_predictions(self, user_id: int, limit: int = 50):
        """Get user's prediction history"""
        ph = self._ph()
        cursor = self._cursor(dict_cursor=True)
        cursor.execute(f'''
            SELECT p.*, f.name as food_name, n.calories, n.protein, n.carbohydrates, n.fats
            FROM predictions p
            LEFT JOIN food_items f ON p.food_item_id = f.id
            LEFT JOIN nutrition_info n ON f.id = n.food_item_id
            WHERE p.user_id = {ph}
            ORDER BY p.prediction_time DESC
            LIMIT {ph}
        ''', (user_id, limit))
        result = []
        for row in self._fetchall(cursor):
            # Normalize timestamp to string for compatibility
            if row.get('prediction_time') and not isinstance(row['prediction_time'], str):
                row['prediction_time'] = row['prediction_time'].isoformat()
            result.append(row)
        return result

    # Nutrition & Food Info
    def get_food_by_name(self, name: str):
        """Get food item by name"""
        ph = self._ph()
        cursor = self._cursor(dict_cursor=True)
        cursor.execute(f'''
            SELECT f.*, n.* FROM food_items f
            JOIN nutrition_info n ON f.id = n.food_item_id
            WHERE f.name = {ph}
        ''', (name,))
        return self._fetchrow(cursor)

    def get_all_foods(self):
        """Get all food items"""
        cursor = self._cursor(dict_cursor=True)
        cursor.execute('''
            SELECT f.id, f.name, f.category, f.meal_type, f.region,
                   f.is_vegetarian, f.is_vegan, f.is_jain, f.spice_level, f.description,
                   n.serving_size, n.serving_size_grams, n.calories, n.protein,
                   n.carbohydrates, n.fats, n.fiber, n.sugar, n.sodium, n.allergens
            FROM food_items f
            JOIN nutrition_info n ON f.id = n.food_item_id
        ''')
        return self._fetchall(cursor)


if __name__ == "__main__":
    import sys
    db = Database()
    if len(sys.argv) > 1 and sys.argv[1] == '--init':
        db.connect()
        db.initialize_database()
    else:
        print("Use --init flag to initialize database")
        print(f"Current backend: {'PostgreSQL' if USE_POSTGRES else 'SQLite'}")
