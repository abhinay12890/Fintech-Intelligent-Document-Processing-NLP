from pathlib import Path
from src.ocr.pdf_reader import is_scanned_pdf, extract_text_from_digital_pdf
from src.ocr.ocr_engine import extract_text_with_ocr
from src.ocr.text_cleaner import clean_ocr_text

def process_pdf(pdf_path):
    if is_scanned_pdf(pdf_path):
        raw = extract_text_with_ocr(pdf_path)
    else:
        raw = extract_text_from_digital_pdf(pdf_path)
    return clean_ocr_text(raw)

