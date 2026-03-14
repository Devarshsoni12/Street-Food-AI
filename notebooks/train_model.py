"""
Training script for Indian Street Food Classifier
This script demonstrates how to train the model with your dataset
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tensorflow as tf
from tensorflow import keras
from src.model import FoodClassifier
from src.preprocessing import ImagePreprocessor
import numpy as np

def create_sample_dataset():
    """Create sample dataset structure"""
    print("Dataset Structure:")
    print("""
    data/
    ├── raw/
    │   ├── samosa/
    │   ├── vada_pav/
    │   ├── pani_puri/
    │   ├── dhokla/
    │   ├── momos/
    │   ├── pav_bhaji/
    │   ├── idli_sambhar/
    │   ├── roti_sabji/
    │   ├── dal_rice/
    │   ├── bhel_puri/
    │   └── noodles/
    """)

def train_model():
    """Train the food classifier model"""
    
    # Initialize classifier
    classifier = FoodClassifier(num_classes=11)
    
    # Build model (choose one)
    # model = classifier.build_mobilenet_model()
    model = classifier.build_ensemble_model()
    
    # Compile model
    classifier.compile_model(learning_rate=0.001)
    
    print("Model Summary:")
    model.summary()
    
    # Data augmentation
    data_augmentation = keras.Sequential([
        keras.layers.RandomFlip("horizontal"),
        keras.layers.RandomRotation(0.1),
        keras.layers.RandomZoom(0.1),
        keras.layers.RandomContrast(0.1),
    ])
    
    # Load dataset (replace with actual data loading)
    # train_ds = keras.utils.image_dataset_from_directory(
    #     'data/raw',
    #     validation_split=0.2,
    #     subset="training",
    #     seed=123,
    #     image_size=(224, 224),
    #     batch_size=32
    # )
    
    # val_ds = keras.utils.image_dataset_from_directory(
    #     'data/raw',
    #     validation_split=0.2,
    #     subset="validation",
    #     seed=123,
    #     image_size=(224, 224),
    #     batch_size=32
    # )
    
    # Callbacks
    callbacks = [
        keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=3,
            min_lr=1e-7
        ),
        keras.callbacks.ModelCheckpoint(
            'models/food_classifier_best.h5',
            monitor='val_accuracy',
            save_best_only=True
        )
    ]
    
    # Train model
    # history = model.fit(
    #     train_ds,
    #     validation_data=val_ds,
    #     epochs=50,
    #     callbacks=callbacks
    # )
    
    # Save final model
    # model.save('models/food_classifier.h5')
    
    print("\nTraining complete!")
    print("Model saved to: models/food_classifier.h5")

if __name__ == "__main__":
    print("=" * 50)
    print("Indian Street Food Classifier - Training Script")
    print("=" * 50)
    
    create_sample_dataset()
    
    print("\nTo train the model:")
    print("1. Organize your images in data/raw/ folder")
    print("2. Uncomment the training code in this script")
    print("3. Run: python notebooks/train_model.py")
    
    # Uncomment to train
    # train_model()
