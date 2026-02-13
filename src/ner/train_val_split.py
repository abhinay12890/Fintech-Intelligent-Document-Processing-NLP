import random
import spacy
from spacy.tokens import DocBin
from pathlib import Path

INPUT_PATH = "data/ner/train.spacy"
TRAIN_OUT = "data/ner/train_split.spacy"
DEV_OUT = "data/ner/val_split.spacy"

DEV_RATIO = 0.15
SEED = 42


def split_spacy_docbin():
    nlp = spacy.blank("en")

    print("Loading DocBin...")
    doc_bin = DocBin().from_disk(INPUT_PATH)
    docs = list(doc_bin.get_docs(nlp.vocab))

    print(f"Total docs: {len(docs)}")

    random.seed(SEED)
    random.shuffle(docs)

    split = int(len(docs) * (1 - DEV_RATIO))
    train_docs = docs[:split]
    dev_docs = docs[split:]

    print(f"Train docs: {len(train_docs)}")
    print(f"Dev docs:   {len(dev_docs)}")

    train_bin = DocBin(store_user_data=True)
    dev_bin = DocBin(store_user_data=True)

    for doc in train_docs:
        train_bin.add(doc)

    for doc in dev_docs:
        dev_bin.add(doc)

    Path(TRAIN_OUT).parent.mkdir(parents=True, exist_ok=True)
    train_bin.to_disk(TRAIN_OUT)
    dev_bin.to_disk(DEV_OUT)

    print("✅ Split completed")
    print(f"Saved: {TRAIN_OUT}")
    print(f"Saved: {DEV_OUT}")


if __name__ == "__main__":
    split_spacy_docbin()
