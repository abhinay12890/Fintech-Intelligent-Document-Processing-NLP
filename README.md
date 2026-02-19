<div align="center">

# 🚀 LexiScan Auto  
### Legal Contract Entity Extraction System

Production-Grade Intelligent Document Processing (OCR + NER + API + Docker)

<br>

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green?logo=fastapi)
![spaCy](https://img.shields.io/badge/spaCy-NER-orange)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue?logo=docker)
![OCR](https://img.shields.io/badge/OCR-Tesseract-lightgrey)

</div>

---

## 📌 Overview

**LexiScan Auto** is a production-ready Intelligent Document Processing (IDP) system designed to extract structured entities from legal contracts.

It supports:

- 📄 Native digital PDFs  
- 🖨 Scanned image-based PDFs (via OCR)

The system automatically extracts:

- Contract Dates  
- Party Names  
- Payment / Liability Terms  
- Termination Clauses  
- Legal & Restriction Clauses  

---

## 🏗 System Architecture

<div align="center">

# 🚀 LexiScan Auto  
### Legal Contract Entity Extraction System

Production-Grade Intelligent Document Processing (OCR + NER + API + Docker)

<br>

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green?logo=fastapi)
![spaCy](https://img.shields.io/badge/spaCy-NER-orange)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue?logo=docker)
![OCR](https://img.shields.io/badge/OCR-Tesseract-lightgrey)

</div>

---

## 📌 Overview

**LexiScan Auto** is a production-ready Intelligent Document Processing (IDP) system designed to extract structured entities from legal contracts.

It supports:

- 📄 Native digital PDFs  
- 🖨 Scanned image-based PDFs (via OCR)

The system automatically extracts:

- Contract Dates  
- Party Names  
- Payment / Liability Terms  
- Termination Clauses  
- Legal & Restriction Clauses  

---

## 🏗 System Architecture

PDF Upload
↓
OCR (Tesseract)
↓
Text Cleaning & Normalization
↓
spaCy Named Entity Recognition Model
↓
Rule-Based Validation
↓
Structured JSON Output

---

## 📂 Project Structure

├── src/
│ ├── api/ # FastAPI REST API
│ ├── ocr/ # OCR + preprocessing pipeline
│ └── ner/ # Rule-based validation
│
├── artifacts/ # Trained spaCy NER model
├── Dockerfile # Containerized deployment
└── README.md

---

## ⚙️ Tech Stack

- Python 3.10  
- spaCy (Custom NER Model)  
- Tesseract OCR  
- pdfplumber  
- FastAPI  
- Uvicorn  
- Docker  

---

## 🚀 Run Locally

Start API server:

```bash
uvicorn src.api.app:app --reload

http://127.0.0.1:8000/docs

🐳 Run With Docker

Build image:

docker build -t lexiscan-auto .


Run container:

docker run -p 8000:8000 lexiscan-auto


Access:

http://localhost:8000/docs

API Endpoint
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

OCR support for scanned contracts

Custom-trained Named Entity Recognition model

Rule-based validation for improved reliability

Fully Dockerized for production deployment

Modular, clean architecture
