import re

def clean_ocr_text(text: str) -> str:
    """
    Production-grade OCR cleanup for legal contracts.
    Fixes spacing, currency, dates, headers/footers, junk chars,
    and removes large OCR gaps while preserving paragraphs.
    """

    # Lowercase for consistency
    text = text.lower()

    # Remove non-ascii junk
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)

    # Remove page numbers
    text = re.sub(r'\n\s*page\s*\d+(\s*of\s*\d+)?\s*\n', '\n', text)
    text = re.sub(r'\n\s*\d+\s*\n', '\n', text)

    # Fix spaced letters: "t h i s" -> "this"
    text = re.sub(r'\b(?:[a-zA-Z]\s+){2,}[a-zA-Z]\b',
              lambda m: m.group(0).replace(" ", ""),
              text)


    # Fix split currency
    text = re.sub(r'\$\s+(\d)', r'$\1', text)
    text = re.sub(r'(\d)\s*,\s*(\d)', r'\1,\2', text)

    # Fix split years
    text = re.sub(r'(\d)\s+(\d)\s+(\d)\s+(\d)', r'\1\2\3\4', text)

    # Fix dates
    text = re.sub(
        r'(january|february|march|april|may|june|july|august|'
        r'september|october|november|december)\s+(\d)\s+(\d)\s*,\s*'
        r'(\d)\s+(\d)\s+(\d)\s+(\d)',
        r'\1 \2\3, \4\5\6\7',
        text
    )

    # Remove table-like spacing
    text = re.sub(r'(\S)\s{4,}(\S)', r'\1 \2', text)

    # 🔥 NEW — Remove massive horizontal gaps (5+ spaces → 1)
    text = re.sub(r' {2,}', ' ', text)

    # 🔥 NEW — Limit vertical gaps (3+ newlines → 2)
    text = re.sub(r'\n{3,}', '\n\n', text)




    # Normalize spaces around newlines
    text = re.sub(r' *\n *', '\n', text)

    # Ensure punctuation spacing
    text = re.sub(r'\s+([.,;:])', r'\1', text)


    return text.strip()
