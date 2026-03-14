import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# ─── CONFIG ───────────────────────────────────────────────────────────────────
DATA_DIR      = 'data/raw'
MODEL_SAVE    = 'models/food_classifier.h5'
IMG_SIZE      = 224
BATCH_SIZE    = 32
EPOCHS_FROZEN = 10   # train with base frozen
EPOCHS_FINE   = 10   # fine-tune top layers
LR_FROZEN     = 1e-3
LR_FINE       = 1e-5

CLASS_NAMES = [
    'Aloo Paratha', 'Burger', 'Chole Bhature', 'Dhokla', 'Dosa',
    'Grilled Sandwich', 'Idli', 'Medul Vada', 'Misal Pav', 'Momos',
    'Pakoda', 'Pani Puri', 'Pav Bhaji', 'Poha', 'Samosa',
    'Sev Puri', 'Vada Pav'
]
NUM_CLASSES = len(CLASS_NAMES)  # 17

# ─── DATA GENERATORS ──────────────────────────────────────────────────────────
train_datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    validation_split=0.2,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2],
    fill_mode='nearest'
)

val_datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    validation_split=0.2
)

print("Loading training data...")
train_gen = train_datagen.flow_from_directory(
    DATA_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='sparse',
    subset='training',
    shuffle=True
)

print("Loading validation data...")
val_gen = val_datagen.flow_from_directory(
    DATA_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='sparse',
    subset='validation',
    shuffle=False
)

print(f"\nClasses found: {train_gen.class_indices}")
print(f"Training samples  : {train_gen.samples}")
print(f"Validation samples: {val_gen.samples}")

# ─── BUILD MODEL ──────────────────────────────────────────────────────────────
print("\nBuilding model...")

base_model = MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,
    weights='imagenet'
)
base_model.trainable = False  # freeze base

inputs  = keras.Input(shape=(IMG_SIZE, IMG_SIZE, 3))
x       = base_model(inputs, training=False)
x       = layers.GlobalAveragePooling2D()(x)
x       = layers.BatchNormalization()(x)
x       = layers.Dense(512, activation='relu')(x)
x       = layers.Dropout(0.4)(x)
x       = layers.Dense(256, activation='relu')(x)
x       = layers.Dropout(0.3)(x)
outputs = layers.Dense(NUM_CLASSES, activation='softmax')(x)

model = keras.Model(inputs, outputs)
model.summary()

# ─── CALLBACKS ────────────────────────────────────────────────────────────────
os.makedirs('models', exist_ok=True)

callbacks = [
    keras.callbacks.ModelCheckpoint(
        MODEL_SAVE,
        monitor='val_accuracy',
        save_best_only=True,
        verbose=1
    ),
    keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True,
        verbose=1
    ),
    keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=3,
        min_lr=1e-7,
        verbose=1
    )
]

# ─── PHASE 1: TRAIN TOP LAYERS (BASE FROZEN) ──────────────────────────────────
print(f"\n{'='*50}")
print("PHASE 1: Training top layers (base frozen)")
print(f"{'='*50}")

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=LR_FROZEN),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

history1 = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=EPOCHS_FROZEN,
    callbacks=callbacks
)

# ─── PHASE 2: FINE-TUNE (UNFREEZE TOP LAYERS OF BASE) ─────────────────────────
print(f"\n{'='*50}")
print("PHASE 2: Fine-tuning top layers of base model")
print(f"{'='*50}")

# Unfreeze top 30 layers of base model
base_model.trainable = True
for layer in base_model.layers[:-30]:
    layer.trainable = False

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=LR_FINE),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

history2 = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=EPOCHS_FINE,
    callbacks=callbacks
)

# ─── RESULTS ──────────────────────────────────────────────────────────────────
print(f"\n{'='*50}")
print("TRAINING COMPLETE!")
print(f"{'='*50}")
print(f"Model saved to: {MODEL_SAVE}")

# Final accuracy
val_loss, val_acc = model.evaluate(val_gen, verbose=0)
print(f"Final Validation Accuracy : {val_acc * 100:.2f}%")
print(f"Final Validation Loss     : {val_loss:.4f}")

# Save class indices mapping
import json
class_indices = train_gen.class_indices
with open('models/class_indices.json', 'w') as f:
    json.dump(class_indices, f, indent=2)
print("Class indices saved to: models/class_indices.json")
