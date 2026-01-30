import re

def clean_ocr_text(text: str) -> str:
    """
    Production-grade OCR cleanup for legal contracts.
    Fixes spacing, currency, dates, headers/footers, and junk chars.
    """

    # Lowercase for consistency
    text = text.lower()

    # Remove non-ascii junk
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)

    # Remove page numbers (common patterns)
    text = re.sub(r'\n\s*page\s*\d+(\s*of\s*\d+)?\s*\n', '\n', text)
    text = re.sub(r'\n\s*\d+\s*\n', '\n', text)

    # Fix split currency: "$ 1 , 000" -> "$1,000"
    text = re.sub(r'\$\s+(\d)', r'$\1', text)
    text = re.sub(r'(\d)\s*,\s*(\d)', r'\1,\2', text)

    # Fix split years: "2 0 2 3" -> "2023"
    text = re.sub(r'(\d)\s+(\d)\s+(\d)\s+(\d)', r'\1\2\3\4', text)

    # Fix dates like "march 1 5 , 2 0 2 2" -> "march 15, 2022"
    text = re.sub(
        r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d)\s+(\d)\s*,\s*(\d)\s+(\d)\s+(\d)\s+(\d)',
        r'\1 \2\3, \4\5\6\7',
        text
    )

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)

    return text.strip()
