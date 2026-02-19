📄 LexiScan Auto – Legal Contract Entity Extraction System
Overview

LexiScan Auto is a production-oriented Intelligent Document Processing (IDP) system designed to extract structured legal entities from contract documents.

The system processes both:

📄 Native digital PDFs

🖨 Scanned image-based PDFs (via OCR)

It automatically extracts key entities such as:

Contract Dates

Party Names

Payment / Financial Terms

Termination Clauses

Legal & Restriction Clauses

The project follows a production-grade MLOps mindset, focusing on reproducibility, modularity, and deployment readiness.

🏗 Architecture
PDF Upload
   ↓
OCR (Tesseract)
   ↓
Text Cleaning & Normalization
   ↓
spaCy Named Entity Recognition Model
   ↓
Rule-Based Postprocessing
   ↓
Structured JSON Response

📂 Project Structure
.
├── src/
│   ├── api/              # FastAPI application (REST endpoint)
│   ├── ocr/              # OCR pipeline and text preprocessing
│   └── ner/              # Entity validation logic
│
├── artifacts/            # Trained spaCy NER model
├── data/                 # Training / evaluation data (if included)
├── Dockerfile            # Containerized deployment
└── README.md

⚙️ Technologies Used

Python 3.10

spaCy (Custom NER)

Tesseract OCR

pdfplumber

FastAPI

Docker

Uvicorn

🚀 Running Locally

Start the API server:

uvicorn src.api.app:app --reload


Open Swagger UI:

http://127.0.0.1:8000/docs


Upload a PDF via the /extract endpoint.

🐳 Running with Docker

Build the container:

docker build -t lexiscan-auto .


Run the container:

docker run -p 8000:8000 lexiscan-auto


Access the API:

http://localhost:8000/docs

🔌 API Endpoint
POST /extract

Accepts:

multipart/form-data

PDF file upload

Returns:

{
  "entities": [
    {"text": "January 1, 2024", "label": "CONTRACT_DATE"},
    {"text": "ABC Corporation", "label": "PARTY"}
  ]
}

🎯 Key Highlights

Handles scanned contracts using OCR

Custom-trained Named Entity Recognition model

Rule-based entity validation for higher reliability

Fully Dockerized for deployment consistency

Designed with production-level structure and modularity
