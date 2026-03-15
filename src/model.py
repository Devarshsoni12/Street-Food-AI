import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV2, EfficientNetB0
import numpy as np

CLASS_NAMES = [
    'Aloo Paratha', 'Burger', 'Chole Bhature', 'Dhokla', 'Dosa',
    'Grilled Sandwich', 'Idli', 'Medu Vada', 'Misal Pav', 'Momos',
    'Pakoda', 'Pani Puri', 'Pav Bhaji', 'Poha', 'Samosa',
    'Sev Puri', 'Vada Pav', 'Unknown'
]

NUM_CLASSES = len(CLASS_NAMES)  # 18

class FoodClassifier:
    def __init__(self, num_classes=NUM_CLASSES, input_shape=(224, 224, 3)):
        self.num_classes = num_classes
        self.input_shape = input_shape
        self.model = None
        self.class_names = CLASS_NAMES

    def build_mobilenet_model(self):
        base_model = MobileNetV2(
            input_shape=self.input_shape,
            include_top=False,
            weights='imagenet'
        )
        base_model.trainable = False

        inputs = keras.Input(shape=self.input_shape)
        x = base_model(inputs, training=False)
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dropout(0.3)(x)
        x = layers.Dense(256, activation='relu')(x)
        x = layers.Dropout(0.2)(x)
        outputs = layers.Dense(self.num_classes, activation='softmax')(x)

        self.model = keras.Model(inputs, outputs)
        return self.model

    def build_efficientnet_model(self):
        base_model = EfficientNetB0(
            input_shape=self.input_shape,
            include_top=False,
            weights='imagenet'
        )
        base_model.trainable = False

        inputs = keras.Input(shape=self.input_shape)
        x = base_model(inputs, training=False)
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dropout(0.3)(x)
        x = layers.Dense(256, activation='relu')(x)
        x = layers.Dropout(0.2)(x)
        outputs = layers.Dense(self.num_classes, activation='softmax')(x)

        self.model = keras.Model(inputs, outputs)
        return self.model

    def compile_model(self, learning_rate=0.001):
        self.model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )

    def load_model(self, model_path):
        self.model = keras.models.load_model(model_path)
        return self.model

    def predict(self, image, return_top_k=3):
        predictions = self.model.predict(image, verbose=0)
        top_k_indices = np.argsort(predictions[0])[-return_top_k:][::-1]

        results = []
        for idx in top_k_indices:
            results.append({
                'class': self.class_names[idx],
                'confidence': float(predictions[0][idx])
            })
        return results

    def predict_with_threshold(self, image, threshold=0.7):
        results = self.predict(image, return_top_k=3)
        if results[0]['confidence'] >= threshold:
            return results[0], results
        else:
            return None, results


class MealTypeClassifier:
    def __init__(self):
        self.food_to_meal = {
            'Aloo Paratha':     ['breakfast', 'lunch'],
            'Burger':           ['lunch', 'snack', 'dinner'],
            'Chole Bhature':    ['breakfast', 'lunch'],
            'Dhokla':           ['breakfast', 'snack'],
            'Dosa':             ['breakfast', 'lunch'],
            'Grilled Sandwich': ['breakfast', 'snack'],
            'Idli':             ['breakfast'],
            'Medu Vada':       ['breakfast', 'snack'],
            'Misal Pav':        ['breakfast', 'lunch'],
            'Momos':            ['snack', 'lunch'],
            'Pakoda':           ['snack'],
            'Pani Puri':        ['snack'],
            'Pav Bhaji':        ['lunch', 'dinner'],
            'Poha':             ['breakfast'],
            'Samosa':           ['breakfast', 'snack'],
            'Sev Puri':         ['snack'],
            'Vada Pav':         ['breakfast', 'snack'],
        }

    def predict_meal_type(self, food_name, time_of_day=None):
        possible_meals = self.food_to_meal.get(food_name, ['snack'])

        if time_of_day:
            hour = time_of_day.hour
            if 5 <= hour < 11 and 'breakfast' in possible_meals:
                return 'breakfast'
            elif 11 <= hour < 16 and 'lunch' in possible_meals:
                return 'lunch'
            elif 16 <= hour < 22 and 'dinner' in possible_meals:
                return 'dinner'

        return possible_meals[0]
