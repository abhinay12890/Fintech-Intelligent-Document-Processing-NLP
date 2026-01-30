from pathlib import Path
from pdf_reader import is_scanned_pdf, extract_text_from_digital_pdf
from ocr_engine import extract_text_with_ocr
from text_cleaner import clean_ocr_text

INPUT_DIR = Path("data/raw_pdfs")
OUTPUT_DIR = Path("data/ocr_text")
OUTPUT_DIR.mkdir(exist_ok=True)

for pdf in INPUT_DIR.glob("*.pdf"):
    print(f"Processing {pdf.name}")

    if is_scanned_pdf(str(pdf)):
        raw = extract_text_with_ocr(str(pdf))
    else:
        raw = extract_text_from_digital_pdf(str(pdf))

    clean = clean_ocr_text(raw)
    (OUTPUT_DIR / f"{pdf.stem}.txt").write_text(clean)

    print(f"Saved {pdf.stem}.txt")
