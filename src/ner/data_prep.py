import json
import spacy
from spacy.tokens import DocBin
from pathlib import Path

LABEL_MAP = {
    "Effective Date": "DATE",
    "Termination Date": "DATE",
    "Parties": "PARTY",
    "Payment Amount": "AMOUNT",
    "Termination Clause": "TERMINATION_CLAUSE"
}

def convert_cuad_to_spacy(cuad_path, output_path):
    nlp = spacy.blank("en")
    doc_bin = DocBin()

    with open(cuad_path, "r") as f:
        cuad = json.load(f)

    for doc in cuad["data"]:
        for para in doc["paragraphs"]:
            text = para["context"]
            spacy_doc = nlp.make_doc(text)
            ents = []

            for qa in para["qas"]:
                if qa.get("is_impossible", False):
                    continue

                label = LABEL_MAP.get(qa["question"])
                if not label:
                    continue

                for ans in qa["answers"]:
                    start = ans["answer_start"]
                    end = start + len(ans["text"])
                    span = spacy_doc.char_span(start, end, label=label)
                    if span:
                        ents.append(span)

            spacy_doc.ents = ents
            doc_bin.add(spacy_doc)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    doc_bin.to_disk(output_path)


if __name__ == "__main__":
    convert_cuad_to_spacy(
        "CUADv1.json",
        "data/ner/train.spacy"
    )
