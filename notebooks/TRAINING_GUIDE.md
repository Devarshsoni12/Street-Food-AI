# Model Training Guide

## Dataset Preparation

### 1. Organize Images
```
data/raw/
├── samosa/          (100+ images)
├── vada_pav/        (100+ images)
├── pani_puri/       (100+ images)
├── dhokla/          (100+ images)
├── momos/           (100+ images)
├── pav_bhaji/       (100+ images)
├── idli_sambhar/    (100+ images)
├── roti_sabji/      (100+ images)
├── dal_rice/        (100+ images)
├── bhel_puri/       (100+ images)
└── noodles/         (100+ images)
```

### 2. Image Requirements
- Format: JPG, PNG, JPEG
- Size: Any (will be resized to 224x224)
- Quality: Clear, well-lit images
- Minimum: 100 images per food
- Recommended: 500+ images per food

## Training Steps

### 1. Prepare Environment
```bash
pip install tensorflow keras opencv-python numpy
```

### 2. Run Training Script
```bash
python notebooks/train_model.py
```

### 3. Monitor Training
- Watch accuracy and loss
- Check for overfitting
- Adjust hyperparameters if needed

### 4. Save Model
Model will be saved to `models/food_classifier.h5`

## Tips for Better Accuracy

1. **More Data**: Collect diverse images
2. **Data Augmentation**: Already implemented
3. **Transfer Learning**: Using pre-trained models
4. **Ensemble**: Combine multiple models
5. **Fine-tuning**: Unfreeze some layers

## Troubleshooting

- **Low Accuracy**: Need more training data
- **Overfitting**: Increase dropout, add regularization
- **Slow Training**: Use GPU, reduce batch size
- **Memory Error**: Reduce batch size

For detailed training code, see `train_model.py`
