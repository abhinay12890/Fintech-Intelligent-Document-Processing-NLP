import re

def clean_ocr_text(text):
    text = text.lower()
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = re.sub(r'\n\s*page\s*\d+(\s*of\s*\d+)?\s*\n', '\n', text)
    text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
    text = re.sub(r'\$\s+(\d)', r'$\1', text)
    text = re.sub(r'(\d)\s*,\s*(\d)', r'\1,\2', text)
    text = re.sub(r'(\d)\s+(\d)\s+(\d)\s+(\d)', r'\1\2\3\4', text)
    return text

