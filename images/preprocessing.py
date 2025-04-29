import cv2
import numpy as np
from PIL import Image

def preprocess_image(image_path):
    # Load and preprocess image
    image = cv2.imread(image_path)
    image_bw = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # CLAHE enhancement
    clahe = cv2.createCLAHE(clipLimit=3, tileGridSize=(10, 10))
    final_img = clahe.apply(image_bw)

    # Brightness increase
    final_img = cv2.add(final_img, 5)

    # Resize and normalize
    final_img = cv2.resize(final_img, (224, 224))
    final_img = np.expand_dims(final_img, axis=-1)
    final_img = np.repeat(final_img, 3, axis=-1)  # Convert to 3 channels
    final_img = final_img / 255.0
    return np.expand_dims(final_img, axis=0)  # Add batch dimension