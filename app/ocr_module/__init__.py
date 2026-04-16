from PIL import Image
from pix2tex.cli import LatexOCR
import torch

class LatexOCRModel:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            print("Loading model...")
            cls._instance = super().__new__(cls)
            cls._instance.model = LatexOCR()  # Load here
        return cls._instance
    
    def predict(self, image_path):
        img = Image.open(image_path)
        return self.model(img)