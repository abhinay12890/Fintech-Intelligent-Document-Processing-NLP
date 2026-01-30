import pytesseract
from pdf2image import convert_from_path

def extract_text_with_ocr(pdf_path: str) -> str:
    images = convert_from_path(pdf_path)
    text = []
    for img in images:
        text.append(pytesseract.image_to_string(img, lang="eng"))
    return "\n".join(text)
