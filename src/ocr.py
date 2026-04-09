import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"



POPPLER_PATH = r"C:\poppler\Library\bin"

def preprocess_image(img):
    # Convert to grayscale
    img = img.convert("L")
    
    # Increase contrast (simple trick)
    img = img.point(lambda x: 0 if x < 140 else 255)
    
    return img

def extract_text(file_path):
    try:
        ext = os.path.splitext(file_path)[1].lower()
        text = ""

        if ext == ".pdf":
            images = convert_from_path(file_path, poppler_path=POPPLER_PATH)
            for img in images:
                img = preprocess_image(img)
                text += pytesseract.image_to_string(img)

        elif ext in [".jpg", ".jpeg", ".png"]:
            img = Image.open(file_path)
            img = preprocess_image(img)
            text = pytesseract.image_to_string(img)

        else:
            print("Unsupported file format")
            return ""

        return text

    except Exception as e:
        print("OCR Error:", e)
        return ""