import pytesseract
from PIL import Image

# CHANGE THIS if your path is different
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    confidence = 0.8 if len(text.strip()) > 10 else 0.3
    return text.strip(), confidence
