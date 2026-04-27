import os
from PIL import Image
from pix2tex.cli import LatexOCR
from ocr_module.preprocess import preprocess_for_ocr
class LatexOCRModel:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            print("Loading model...")
            cls._instance = super().__new__(cls)
            cls._instance.model = LatexOCR()
        return cls._instance
    
    def predict(self, image_path):
        preprocess = preprocess_for_ocr(image_path)
        pil_img = Image.fromarray(preprocess)
        result = self.model(pil_img)
        return result