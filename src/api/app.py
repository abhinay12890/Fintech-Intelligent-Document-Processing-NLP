from fastapi import FastAPI, UploadFile, File
import shutil
import os
import spacy

from src.ocr.run_ocr import process_pdf
from src.ner.postprocess import postprocess_entities

app = FastAPI()
MODEL_PATH = "artifacts/ner_model"
nlp = spacy.load(MODEL_PATH)


@app.post("/extract")
async def extract_entities(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = process_pdf(temp_path)
    doc = nlp(text)

    raw_entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
    cleaned_entities = postprocess_entities(raw_entities)

    os.remove(temp_path)

    return {"entities": cleaned_entities}

