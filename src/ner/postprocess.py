import re

def is_valid_date(text):
    return re.search(r'\b\d{4}-\d{2}-\d{2}\b', text) is not None

def is_valid_amount(text):
    return re.search(r'\$\d+', text) is not None

def is_valid_party(text):
    return len(text.split()) >= 2

def is_valid_termination(text):
    keywords = ["terminate", "termination", "expire", "breach"]
    return any(k in text.lower() for k in keywords)

def postprocess_entities(entities):
    cleaned = []
    for ent in entities:
        text = ent["text"]
        label = ent["label"]

        if label == "DATE" and is_valid_date(text):
            cleaned.append(ent)
        elif label == "AMOUNT" and is_valid_amount(text):
            cleaned.append(ent)
        elif label == "PARTY" and is_valid_party(text):
            cleaned.append(ent)
        elif label == "TERMINATION_CLAUSE" and is_valid_termination(text):
            cleaned.append(ent)

    return cleaned

