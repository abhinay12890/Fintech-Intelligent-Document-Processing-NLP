import spacy
from spacy.tokens import DocBin
from spacy.training import Example
from pathlib import Path
import random

TRAIN_DATA_PATH = "data/ner/train.spacy"
MODEL_OUTPUT_DIR = "artifacts/ner_model"

EPOCHS = 2
MAX_DOCS = 500
BATCH_SIZE = 8

def train_ner():
    nlp = spacy.load(
        "en_core_web_sm",
        disable=["parser", "tagger", "lemmatizer"]
    )

    doc_bin = DocBin().from_disk(TRAIN_DATA_PATH)
    docs = list(doc_bin.get_docs(nlp.vocab))[:MAX_DOCS]

    ner = nlp.get_pipe("ner")

    for doc in docs:
        for ent in doc.ents:
            ner.add_label(ent.label_)

    optimizer = nlp.initialize()

    for epoch in range(EPOCHS):
        random.shuffle(docs)
        losses = {}

        for i in range(0, len(docs), BATCH_SIZE):
            batch = docs[i:i + BATCH_SIZE]
            examples = [
                Example.from_dict(
                    doc,
                    {"entities": [(e.start_char, e.end_char, e.label_) for e in doc.ents]}
                )
                for doc in batch
            ]

            nlp.update(examples, sgd=optimizer, losses=losses)

        print(f"Epoch {epoch + 1} - Losses: {losses}")

    Path(MODEL_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    nlp.to_disk(MODEL_OUTPUT_DIR)
    print("Optimized model saved")

if __name__ == "__main__":
    train_ner()
