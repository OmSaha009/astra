import cv2
import numpy
from PIL import Image
from core.logging import setup_logger

logger = setup_logger(__name__)

def preprocess_for_ocr(image_path: str) -> Image.Image:
    
    img = cv2.imread(image_path)
    if img is None:
        logger.error(f"OCR Preprocessor: Could not load image {image_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    h, w = gray.shape
    if w < 300:
        scale = 300/w
        new_w = 300
        new_h = int(h*scale)
        gray = cv2.resize(gray, (new_w, new_h))

    gray_3channel = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    return gray_3channel