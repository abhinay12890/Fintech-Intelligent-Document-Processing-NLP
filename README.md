# 📄 Fintech-Intelligent-Document-Processing-NLP – Legal NER + OCR Pipeline

## Project Overview

This project implements a production-ready, end-to-end **Legal Contract Intelligence Pipeline** built on the **CUAD (Contract Understanding Atticus Dataset)**.

The system performs:

- OCR fallback for scanned PDFs  
- Structured text cleaning for legal contracts  
- Sliding-window NER training for long documents  
- GPU-accelerated spaCy training  
- Custom evaluation pipeline  
- Model artifact export for downstream integration  

The goal is to build a **contract clause extraction engine** that can process both digital and scanned PDFs and extract structured legal entities such as:

- PARTY  
- CONTRACT_DATE  
- LIABILITY  
- PAYMENT_TERM  
- LICENSE_TERM  
- IP_OWNERSHIP  
- RESTRICTION  
- TERMINATION  
- LEGAL  

This project focuses on:

- Label engineering & class consolidation  
- Long-document chunking  
- GPU memory optimization  
- Early stopping & best-model checkpointing  
- Hybrid OCR + NLP architecture  

---

## Dataset

**Source:** CUAD v1 (Contract Understanding Atticus Dataset)  
**Domain:** Legal contracts  
**Task:** Named Entity Recognition (Clause Extraction)  

Original CUAD contains 40+ fine-grained labels.  
These were consolidated into higher-level semantic categories for stability and improved generalization.

---

## Project Structure
```
├── data/
│   ├── raw_pdfs/                # Local PDFs for OCR testing
│   ├── ocr_text/                # Cleaned OCR outputs
│   └── ner/
│       ├── train.spacy          # Processed CUAD dataset
│       ├── train_split.spacy    # Training split
│       └── val_split.spacy      # Validation split
│
├── ocr/
│   ├── run_ocr.py               # OCR pipeline entry point
│   ├── pdf_reader.py            # Digital PDF extraction
│   ├── ocr_engine.py            # Tesseract OCR fallback
│   └── text_cleaner.py          # Legal OCR cleanup
│
├── data_prep.py                 # CUAD → spaCy DocBin conversion
├── train_val_split.py           # Train/Validation split
├── train_spacy_gpy.py           # GPU NER training script
├── evaluate.py                  # Model evaluation script
├── retrain.py                   # To retrain the model in-case of OOM during training
│
├── artifacts/
│   └── ner_web_gpu/             # Saved trained model
│
└── README.md                    # This file
```

---

## Data Preprocessing

### Label Engineering

CUAD labels were merged into broader legal categories.

Example mappings:

- AGREEMENT_DATE → CONTRACT_DATE  
- NON_COMPETE → RESTRICTION  
- CAP_ON_LIABILITY → LIABILITY  
- LICENSE_GRANT → LICENSE_TERM  

This reduces label sparsity and improves training stability.

---

### Span Processing

- Exact span reconstruction using `char_span`
- Hard span validation:
  - No newline spans
  - No trailing punctuation
  - Token-length limits
- Overlap resolution using `filter_spans`

---

### Train/Validation Split

- 85% training  
- 15% validation  
- Random seed for reproducibility  
- Saved as `.spacy` DocBin files inside `data/ner/`

---

## Model Training

Training is implemented in `train_spacy_gpy.py`.

### Key Design Decisions

- **Base Model:** `en_core_web_sm`  
- **GPU Training:** Forced via `spacy.require_gpu()`  
- **Epochs:** 40  
- **Early Stopping Patience:** 7  
- **Dropout:** 0.15  

---

### Long Document Handling (Sliding Window)

Legal contracts are long documents.

To handle memory and sequence limits:

- `MAX_TOKENS = 1000`  
- `OVERLAP = 200`  

Sliding window chunking ensures:

- Stable GPU memory usage  
- Preserved entity continuity  
- Efficient gradient updates  

---

### Training Strategy

- Removed default NER
- Added custom NER head
- Added labels dynamically from training data
- Batched updates using `minibatch`
- Evaluated per epoch
- Saved best model based on F1 score

Model artifacts are saved in: `artifacts/ner_web_gpu/`

---

## Model Evaluation

Evaluation is implemented in `evaluate.py`.

Evaluation logic:

- Load trained model
- Load validation DocBin
- Exact span matching
- Binary precision / recall / F1 computation

Metrics printed:

- Precision  
- Recall  
- F1-score  

---

## OCR Pipeline (Pre-Integration Layer)

The OCR module allows processing local PDFs before feeding them into the trained NER model.

### Hybrid PDF Processing

`run_ocr.py`:

1. Detect whether PDF is digital or scanned  
2. Use:
   - `pdfplumber` for digital PDFs
   - `pytesseract` + `pdf2image` for scanned PDFs  
3. Apply legal-focused text cleaning  
4. Save cleaned `.txt` files  

---

### OCR Cleanup Features

`text_cleaner.py` performs:

- Removal of non-ASCII junk  
- Page number removal  
- Currency normalization  
- Date reconstruction  
- Split-letter fixes (e.g., `t h i s → this`)  
- Table spacing normalization  
- Horizontal & vertical whitespace control  

This prepares OCR text for future NER integration.

---

## Deployment-Ready Design

While this repository currently focuses on model training and OCR preprocessing, the architecture supports:

- Contract ingestion  
- Text extraction  
- Cleaning  
- Entity extraction  
- Structured JSON output (future integration)  

---

## How To Run

Convert CUAD to spaCy format `python data_prep.py`

Split into train/validation `python train_val_split.py`

Train the model (GPU required) `python train_spacy_gpy.py`

Best model will be saved inside: `artifacts/ner_web_gpu/`

Evaluate model: `python evaluate.py`

---
Dockerized the pipeline to integrate both text based and pdf based inputs for entity recognition
Image: [fintech-doc on Docker Hub](https://hub.docker.com/repository/docker/abhinay1289/fintech-doc/general)

`docker pull abhinay1289/fintech-doc:latest`
`docker run -p 8000:8000 fintech-doc:latest`

---

## Technical Highlights

- End-to-end Intelligent Document Processing pipeline  
- GPU-accelerated spaCy NER training  
- Sliding-window training for long legal documents  
- Custom label consolidation strategy  
- Hybrid digital + OCR PDF ingestion  
- Early stopping with best-model checkpointing  
- Modular pipeline design  

---

## Future Enhancements

- Transformer-based model (`en_core_web_trf`)  
- Per-label performance reporting  
- Confidence thresholding  
- Structured JSON export  
- RAG-based clause retrieval  
- Layout-aware OCR integration  

---

## Contributor

**Kalavakuri Abhinay**  
label engineering, NER training and documentation.
**Prathmesh Yadav**
OCR pipeline, evaluation framework, deployment and dockerization

---

## License

This project uses the CUAD dataset for research and educational purposes.


