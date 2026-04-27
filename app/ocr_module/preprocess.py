import cv2
import numpy as np
from PIL import Image
from core.logging import setup_logger

logger = setup_logger(__name__)

def preprocess_for_ocr(image_path: str) -> Image.Image:
    
    img = cv2.imread(image_path)
    if img is None:
        logger.error(f"OCR Preprocessor: Could not load image {image_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    brightness = np.mean(gray)
    print(f"Brightness: {brightness:.1f}")
    
    if brightness < 127:
        print("Dark background detected → inverting")
        gray = cv2.bitwise_not(gray)
    
    h, w = gray.shape
    if w < 300:
        scale = 300 / w
        new_w = 300
        new_h = int(h * scale)
        gray = cv2.resize(gray, (new_w, new_h))
    
    if np.std(gray) < 50: 
        print("Low contrast detected → applying CLAHE")
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        gray = clahe.apply(gray)

    gray_3channel = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    return gray_3channel