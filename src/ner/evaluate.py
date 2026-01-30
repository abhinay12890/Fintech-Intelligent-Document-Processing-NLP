import spacy
from spacy.tokens import DocBin
from sklearn.metrics import precision_recall_fscore_support

MODEL_PATH = "artifacts/ner_model"
DATA_PATH = "data/ner/train.spacy"

def extract_entities(doc):
    return set((ent.start_char, ent.end_char, ent.label_) for ent in doc.ents)

def evaluate_ner():
    # Load trained model
    nlp = spacy.load(MODEL_PATH)

    # Load gold data
    doc_bin = DocBin().from_disk(DATA_PATH)
    gold_docs = list(doc_bin.get_docs(nlp.vocab))

    y_true = []
    y_pred = []

    for gold_doc in gold_docs:
        pred_doc = nlp(gold_doc.text)

        gold_ents = extract_entities(gold_doc)
        pred_ents = extract_entities(pred_doc)

        all_ents = gold_ents.union(pred_ents)

        for ent in all_ents:
            y_true.append(1 if ent in gold_ents else 0)
            y_pred.append(1 if ent in pred_ents else 0)

    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average="binary"
    )

    print("NER Evaluation Results")
    print("----------------------")
    print(f"Precision: {precision:.3f}")
    print(f"Recall:    {recall:.3f}")
    print(f"F1-score:  {f1:.3f}")

if __name__ == "__main__":
    evaluate_ner()
