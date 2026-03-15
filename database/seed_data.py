import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from src.database import Database

def seed_foods():
    db = Database()
    db.connect()
    cursor = db.conn.cursor()

    # Clear existing food data
    cursor.execute("DELETE FROM nutrition_info")
    cursor.execute("DELETE FROM food_items")
    db.conn.commit()

    foods_data = [
        {
            'name': 'Aloo Paratha',
            'category': 'main_course', 'meal_type': 'breakfast,lunch',
            'region': 'north', 'is_vegetarian': True, 'is_vegan': False,
            'is_jain': False, 'spice_level': 3,
            'description': 'Whole wheat flatbread stuffed with spiced potato',
            'nutrition': {'serving_size': '2 pieces', 'serving_size_grams': 200,
                          'calories': 400, 'protein': 9, 'carbohydrates': 58,
                          'fats': 15, 'fiber': 5, 'sugar': 2, 'sodium': 480,
                          'allergens': ['gluten', 'dairy']}
        },
        {
            'name': 'Burger',
            'category': 'street_food', 'meal_type': 'lunch,snack,dinner',
            'region': 'all', 'is_vegetarian': True, 'is_vegan': False,
            'is_jain': False, 'spice_level': 2,
            'description': 'Veg burger with bun and toppings',
            'nutrition': {'serving_size': '1 piece', 'serving_size_grams': 180,
                          'calories': 350, 'protein': 10, 'carbohydrates': 45,
                          'fats': 14, 'fiber': 3, 'sugar': 6, 'sodium': 620,
                          'allergens': ['gluten', 'dairy']}
        },
        {
            'name': 'Chole Bhature',
            'category': 'main_course', 'meal_type': 'breakfast,lunch',
            'region': 'north', 'is_vegetarian': True, 'is_vegan': False,
            'is_jain': False, 'spice_level': 4,
            'description': 'Spicy chickpea curry with fried bread',
            'nutrition': {'serving_size': '1 plate', 'serving_size_grams': 350,
                          'calories': 550, 'protein': 16, 'carbohydrates': 72,
                          'fats': 22, 'fiber': 10, 'sugar': 5, 'sodium': 780,
                          'allergens': ['gluten']}
        },
        {
            'name': 'Dhokla',
            'category': 'street_food', 'meal_type': 'breakfast,snack',
            'region': 'gujarat', 'is_vegetarian': True, 'is_vegan': True,
            'is_jain': True, 'spice_level': 2,
            'description': 'Steamed fermented gram flour cake',
            'nutrition': {'serving_size': '4 pieces', 'serving_size_grams': 150,
                          'calories': 220, 'protein': 8, 'carbohydrates': 38,
                          'fats': 4, 'fiber': 4, 'sugar': 3, 'sodium': 380,
                          'allergens': []}
        },
        {
            'name': 'Dosa',
            'category': 'main_course', 'meal_type': 'breakfast,lunch',
            'region': 'south', 'is_vegetarian': True, 'is_vegan': True,
            'is_jain': False, 'spice_level': 2,
            'description': 'Crispy fermented rice and lentil crepe',
            'nutrition': {'serving_size': '1 piece', 'serving_size_grams': 150,
                          'calories': 200, 'protein': 5, 'carbohydrates': 38,
                          'fats': 4, 'fiber': 2, 'sugar': 1, 'sodium': 320,
                          'allergens': []}
        },
        {
            'name': 'Grilled Sandwich',
            'category': 'street_food', 'meal_type': 'breakfast,snack',
            'region': 'all', 'is_vegetarian': True, 'is_vegan': False,
            'is_jain': False, 'spice_level': 2,
            'description': 'Grilled bread sandwich with vegetables and cheese',
            'nutrition': {'serving_size': '1 piece', 'serving_size_grams': 160,
                          'calories': 280, 'protein': 9, 'carbohydrates': 36,
                          'fats': 11, 'fiber': 3, 'sugar': 4, 'sodium': 520,
                          'allergens': ['gluten', 'dairy']}
        },
        {
            'name': 'Idli',
            'category': 'main_course', 'meal_type': 'breakfast',
            'region': 'south', 'is_vegetarian': True, 'is_vegan': True,
            'is_jain': False, 'spice_level': 1,
            'description': 'Steamed rice and lentil cakes',
            'nutrition': {'serving_size': '3 pieces', 'serving_size_grams': 150,
                          'calories': 150, 'protein': 5, 'carbohydrates': 30,
                          'fats': 1, 'fiber': 2, 'sugar': 1, 'sodium': 280,
                          'allergens': []}
        },
        {
            'name': 'Medu Vada',
            'category': 'street_food', 'meal_type': 'breakfast,snack',
            'region': 'south', 'is_vegetarian': True, 'is_vegan': True,
            'is_jain': False, 'spice_level': 3,
            'description': 'Crispy fried lentil doughnut',
            'nutrition': {'serving_size': '2 pieces', 'serving_size_grams': 100,
                          'calories': 240, 'protein': 7, 'carbohydrates': 28,
                          'fats': 12, 'fiber': 3, 'sugar': 1, 'sodium': 360,
                          'allergens': []}
        },
        {
            'name': 'Misal Pav',
            'category': 'main_course', 'meal_type': 'breakfast,lunch',
            'region': 'maharashtra', 'is_vegetarian': True, 'is_vegan': False,
            'is_jain': False, 'spice_level': 5,
            'description': 'Spicy sprouted lentil curry with bread',
            'nutrition': {'serving_size': '1 plate', 'serving_size_grams': 300,
                          'calories': 420, 'protein': 14, 'carbohydrates': 60,
                          'fats': 13, 'fiber': 9, 'sugar': 4, 'sodium': 680,
                          'allergens': ['gluten']}
        },
        {
            'name': 'Momos',
            'category': 'street_food', 'meal_type': 'snack,lunch',
            'region': 'north', 'is_vegetarian': True, 'is_vegan': False,
            'is_jain': False, 'spice_level': 3,
            'description': 'Steamed dumplings with vegetable filling',
            'nutrition': {'serving_size': '6 pieces', 'serving_size_grams': 150,
                          'calories': 210, 'protein': 7, 'carbohydrates': 35,
                          'fats': 5, 'fiber': 3, 'sugar': 2, 'sodium': 450,
                          'allergens': ['gluten', 'soy']}
        },
        {
            'name': 'Pakoda',
            'category': 'street_food', 'meal_type': 'snack',
            'region': 'all', 'is_vegetarian': True, 'is_vegan': True,
            'is_jain': False, 'spice_level': 3,
            'description': 'Crispy fried gram flour fritters with vegetables',
            'nutrition': {'serving_size': '6 pieces', 'serving_size_grams': 120,
                          'calories': 280, 'protein': 6, 'carbohydrates': 30,
                          'fats': 16, 'fiber': 3, 'sugar': 2, 'sodium': 420,
                          'allergens': []}
        },
        {
            'name': 'Pani Puri',
            'category': 'street_food', 'meal_type': 'snack',
            'region': 'all', 'is_vegetarian': True, 'is_vegan': True,
            'is_jain': True, 'spice_level': 5,
            'description': 'Crispy hollow puri filled with spicy water',
            'nutrition': {'serving_size': '6 pieces', 'serving_size_grams': 90,
                          'calories': 180, 'protein': 4, 'carbohydrates': 32,
                          'fats': 4, 'fiber': 2, 'sugar': 5, 'sodium': 380,
                          'allergens': ['gluten']}
        },
        {
            'name': 'Pav Bhaji',
            'category': 'street_food', 'meal_type': 'lunch,dinner',
            'region': 'mumbai', 'is_vegetarian': True, 'is_vegan': False,
            'is_jain': False, 'spice_level': 4,
            'description': 'Spiced mashed vegetables with buttered bread',
            'nutrition': {'serving_size': '1 plate', 'serving_size_grams': 300,
                          'calories': 450, 'protein': 10, 'carbohydrates': 55,
                          'fats': 20, 'fiber': 6, 'sugar': 8, 'sodium': 680,
                          'allergens': ['gluten', 'dairy']}
        },
        {
            'name': 'Poha',
            'category': 'main_course', 'meal_type': 'breakfast',
            'region': 'central', 'is_vegetarian': True, 'is_vegan': True,
            'is_jain': False, 'spice_level': 2,
            'description': 'Flattened rice cooked with spices and vegetables',
            'nutrition': {'serving_size': '1 plate', 'serving_size_grams': 200,
                          'calories': 250, 'protein': 5, 'carbohydrates': 48,
                          'fats': 5, 'fiber': 3, 'sugar': 3, 'sodium': 380,
                          'allergens': ['peanuts']}
        },
        {
            'name': 'Samosa',
            'category': 'street_food', 'meal_type': 'breakfast,snack',
            'region': 'north', 'is_vegetarian': True, 'is_vegan': False,
            'is_jain': False, 'spice_level': 3,
            'description': 'Crispy fried pastry with spiced potato filling',
            'nutrition': {'serving_size': '2 pieces', 'serving_size_grams': 100,
                          'calories': 262, 'protein': 4, 'carbohydrates': 28,
                          'fats': 15, 'fiber': 2, 'sugar': 1, 'sodium': 422,
                          'allergens': ['gluten']}
        },
        {
            'name': 'Sev Puri',
            'category': 'street_food', 'meal_type': 'snack',
            'region': 'mumbai', 'is_vegetarian': True, 'is_vegan': True,
            'is_jain': True, 'spice_level': 3,
            'description': 'Crispy puri topped with sev, potatoes and chutneys',
            'nutrition': {'serving_size': '6 pieces', 'serving_size_grams': 120,
                          'calories': 220, 'protein': 5, 'carbohydrates': 36,
                          'fats': 7, 'fiber': 3, 'sugar': 6, 'sodium': 480,
                          'allergens': ['gluten', 'peanuts']}
        },
        {
            'name': 'Vada Pav',
            'category': 'street_food', 'meal_type': 'breakfast,snack',
            'region': 'mumbai', 'is_vegetarian': True, 'is_vegan': False,
            'is_jain': False, 'spice_level': 4,
            'description': 'Spiced potato fritter in a bun',
            'nutrition': {'serving_size': '1 piece', 'serving_size_grams': 120,
                          'calories': 286, 'protein': 6, 'carbohydrates': 38,
                          'fats': 12, 'fiber': 3, 'sugar': 3, 'sodium': 520,
                          'allergens': ['gluten']}
        },
    ]

    for food in foods_data:
        cursor.execute('''
            INSERT INTO food_items (name, category, meal_type, region, is_vegetarian,
                                   is_vegan, is_jain, spice_level, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (food['name'], food['category'], food['meal_type'], food['region'],
              food['is_vegetarian'], food['is_vegan'], food['is_jain'],
              food['spice_level'], food['description']))

        food_id = cursor.lastrowid
        n = food['nutrition']
        cursor.execute('''
            INSERT INTO nutrition_info (food_item_id, serving_size, serving_size_grams,
                                       calories, protein, carbohydrates, fats, fiber,
                                       sugar, sodium, allergens)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (food_id, n['serving_size'], n['serving_size_grams'],
              n['calories'], n['protein'], n['carbohydrates'], n['fats'],
              n['fiber'], n['sugar'], n['sodium'], json.dumps(n['allergens'])))

    db.conn.commit()
    print(f"Seeded {len(foods_data)} food items successfully!")
    db.close()


def create_admin():
    db = Database()
    db.connect()
    admin_id = db.create_user(
        username='admin',
        email='admin@streetfood.ai',
        password='admin123',
        full_name='System Administrator',
        is_admin=True
    )
    if admin_id:
        print("Admin created! Email: admin@streetfood.ai | Password: admin123")
    else:
        print("Admin already exists.")
    db.close()


if __name__ == "__main__":
    print("Seeding database...")
    seed_foods()
    create_admin()
    print("Done!")
