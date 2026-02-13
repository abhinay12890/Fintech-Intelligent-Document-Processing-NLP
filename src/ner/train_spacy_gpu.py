import os
# ---- GPU memory stabilizers ----
os.environ["THINC_GPU_ALLOCATOR"] = "cuda"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"


import cupy
import torch
torch.set_float32_matmul_precision("high")

import spacy
import random
import gc

from spacy.tokens import DocBin,Doc, Span
from spacy.training import Example
from pathlib import Path
from spacy.scorer import Scorer
from spacy.util import minibatch


spacy.require_gpu()   # FORCE GPU
torch.cuda.empty_cache()


TRAIN_DATA_PATH = "data/ner/train_split.spacy"
VAL_DATA_PATH = "data/ner/val_split.spacy"
MODEL_OUTPUT_DIR = "artifacts/ner_web_gpu"

EPOCHS = 40
PATIENCE=7
DROPOUT= 0.15


MAX_TOKENS = 1000
OVERLAP = 200   


def chunk_doc(doc, max_tokens=MAX_TOKENS, overlap=OVERLAP):
    chunks = []

    start = 0
    while start < len(doc):
        end = min(start + max_tokens, len(doc))

        # Create subdoc
        #words = [t.text for t in doc[start:end]]
        #spaces = [bool(t.whitespace_) for t in doc[start:end]]

        #subdoc = Doc(doc.vocab, words=words, spaces=spaces)
        subdoc= doc[start:end].as_doc()

        # Rebuild entities safely
        ents = []
        for ent in doc.ents:

            if ent.start >= start and ent.end <= end:
                span = Span(
                    subdoc,
                    ent.start - start,
                    ent.end - start,
                    label=ent.label_
                )
                ents.append(span)

        if len(ents) > 0:
            subdoc.ents = ents
            chunks.append(subdoc)

        start += max_tokens - overlap   # ← SLIDING WINDOW

    return chunks


def load_docs_chunked(path, vocab):
    db = DocBin().from_disk(path)
    docs = list(db.get_docs(vocab))

    chunked_docs = []

    for doc in docs:
        if len(doc) <= MAX_TOKENS:
            chunked_docs.append(doc)
        else:
            chunked_docs.extend(chunk_doc(doc))

    print(f"Original docs: {len(docs)}")
    print(f"After chunking: {len(chunked_docs)}")

    return chunked_docs


def evaluate(nlp, dev_docs):

    examples = []

    texts = [doc.text for doc in dev_docs]

    with torch.no_grad():
        preds = list(nlp.pipe(texts, batch_size=4))

    for pred, ref in zip(preds, dev_docs):
        examples.append(Example(pred, ref))

    scorer = Scorer()
    scores = scorer.score(examples)

    return scores["ents_f"], scores["ents_p"], scores["ents_r"]


def train():
    nlp=spacy.load("en_core_web_sm")

    if "ner" in nlp.pipe_names:
        nlp.remove_pipe("ner")
    
    ner=nlp.add_pipe("ner")
    nlp.max_length=400000
    #tok2vec=nlp.add_pipe("tok2vec")
    print("Loading Datasets...")
    train_docs = load_docs_chunked(TRAIN_DATA_PATH, nlp.vocab)
    
    db=DocBin().from_disk(VAL_DATA_PATH)
    val_docs=list(db.get_docs(nlp.vocab))
    

    print("Train docs: ",len(train_docs))
    print("Val docs: ",len(val_docs))



    disable=["tagger","parser","attribute_ruler","lemmatizer"]
    nlp.disable_pipes(*disable)

    labels = {ent.label_ for doc in train_docs for ent in doc.ents}

    for label in labels:
        ner.add_label(label)
    
    print("NER LABELS: ",ner.labels)


    with nlp.select_pipes(enable=["ner"]):
        optimizer=nlp.initialize()

    best_f1=-1
    patience_counter=0

    random.shuffle(train_docs)

    train_examples = []

    for doc in train_docs:
        ents = [(ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]
        train_examples.append(
            Example.from_dict(nlp.make_doc(doc.text),{"entities": ents}))


    print("Starting Training...")

    for epoch in range(EPOCHS):
        random.shuffle(train_examples)

        losses={}

        batches=minibatch(train_examples,size=4)

        for batch in batches:
            nlp.update(batch,sgd=optimizer,drop=DROPOUT,losses=losses)
        
        f1,precision,recall=evaluate(nlp,val_docs)
        print(f"""
              Epoch {epoch+1}
              Loss: {losses['ner']:.0f}
              F1: {f1:.3f}
              Precision: {precision:.3f}
              Recall: {recall:.3f}""")
        torch.cuda.empty_cache()
        cupy.get_default_memory_pool().free_all_blocks()
        gc.collect()
        if f1>best_f1:
            best_f1=f1
            patience_counter=0
            Path(MODEL_OUTPUT_DIR).mkdir(parents=True,exist_ok=True)
            nlp.to_disk(MODEL_OUTPUT_DIR)
            print("Best Model Saved...")
        else:
            patience_counter+=1
            print(f"No improvement ({patience_counter}/{PATIENCE})")
        if patience_counter>=PATIENCE:
            print("Early Stopping triggered...")
            break

if __name__=="__main__":
    train()