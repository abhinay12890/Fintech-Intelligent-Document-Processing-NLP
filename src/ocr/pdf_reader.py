import pdfplumber

def is_scanned_pdf(pdf_path: str) -> bool:
    """
    Returns True if:
    - PDF has no extractable text
    - OR pdfplumber fails (corrupt / image-only PDF)
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text and text.strip():
                    return False
        return True
    except Exception:
        # If pdfplumber crashes, treat as scanned
        return True


def extract_text_from_digital_pdf(pdf_path: str) -> str:
    text_pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                text_pages.append(text)
    return "\n".join(text_pages)
