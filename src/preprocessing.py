import cv2
import numpy as np
from PIL import Image
import tensorflow as tf

class ImagePreprocessor:
    def __init__(self, target_size=(224, 224)):
        self.target_size = target_size
    
    def preprocess_for_model(self, image):
        """Preprocess image for model inference"""
        # Resize
        img = cv2.resize(image, self.target_size)
        
        # Normalize to [0, 1]
        img = img.astype(np.float32) / 255.0
        
        # Add batch dimension
        img = np.expand_dims(img, axis=0)
        
        return img
    
    def load_and_preprocess(self, image_path):
        """Load image from path and preprocess"""
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return self.preprocess_for_model(img)
    
    def preprocess_pil_image(self, pil_image):
        """Preprocess PIL Image"""
        img = np.array(pil_image)
        if img.shape[-1] == 4:  # RGBA
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
        return self.preprocess_for_model(img)
    
    def enhance_image(self, image):
        """Apply image enhancement techniques"""
        # Convert to LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Merge channels
        enhanced = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2RGB)
        
        return enhanced
    
    def detect_food_region(self, image):
        """Detect and crop food region (simple implementation)"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Edge detection
        edges = cv2.Canny(blurred, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Get largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            
            # Add padding
            padding = 20
            x = max(0, x - padding)
            y = max(0, y - padding)
            w = min(image.shape[1] - x, w + 2 * padding)
            h = min(image.shape[0] - y, h + 2 * padding)
            
            return image[y:y+h, x:x+w]
        
        return image
    
    def augment_image(self, image):
        """Apply data augmentation"""
        augmented = []
        
        # Original
        augmented.append(image)
        
        # Horizontal flip
        augmented.append(cv2.flip(image, 1))
        
        # Rotation
        rows, cols = image.shape[:2]
        for angle in [-10, 10]:
            M = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
            rotated = cv2.warpAffine(image, M, (cols, rows))
            augmented.append(rotated)
        
        # Brightness adjustment
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        hsv = hsv.astype(np.float32)
        hsv[:, :, 2] = hsv[:, :, 2] * 1.2
        hsv = np.clip(hsv, 0, 255).astype(np.uint8)
        bright = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        augmented.append(bright)
        
        return augmented
