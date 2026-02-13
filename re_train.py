import os
# ---- GPU memory stabilizers ----
os.environ["THINC_GPU_ALLOCATOR"] = "cuda"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"


import cupy
import torch
torch.set_float32_matmul_precision("high")
torch.backends.cudnn.benchmark = True
torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True


import spacy
import random
import gc

from spacy.tokens import DocBin
from spacy.training import Example
from pathlib import Path
from spacy.scorer import Scorer
from spacy.util import minibatch


spacy.require_gpu()   # FORCE GPU
torch.cuda.empty_cache()


TRAIN_DATA_PATH = "data/ner/train_split.spacy"
VAL_DATA_PATH = "data/ner/val_split.spacy"
LOAD_MODEL_PATH="artifacts/ner_web_gpu"
MODEL_OUTPUT_DIR = "artifacts/ner_web_md_gpu_19_continued"

EPOCHS = 30
PATIENCE=7
DROPOUT= 0.15

MAX_TOKENS = 1500   # SAFE for 4GB GPU

def load_docs(path, vocab):
    db = DocBin().from_disk(path)
    docs = list(db.get_docs(vocab))

    filtered_docs = [d for d in docs if len(d) < MAX_TOKENS]

    print(f"Dropped {len(docs) - len(filtered_docs)} long docs")

    return filtered_docs


def evaluate(nlp, dev_docs):

    examples = []

    texts = [doc.text for doc in dev_docs]

    with torch.no_grad():
        preds = list(nlp.pipe(texts, batch_size=2))

    for pred, ref in zip(preds, dev_docs):
        examples.append(Example(pred, ref))

    scorer = Scorer()
    scores = scorer.score(examples)

    return scores["ents_f"], scores["ents_p"], scores["ents_r"]


def train():
    nlp=spacy.load(LOAD_MODEL_PATH)
    nlp.max_length=400000
    #tok2vec=nlp.add_pipe("tok2vec")
    ner=nlp.get_pipe("ner")
    print("Loading Datasets...")
    train_docs=load_docs(TRAIN_DATA_PATH,nlp.vocab)
    val_docs=load_docs(VAL_DATA_PATH,nlp.vocab)

    print("Train docs: ",len(train_docs))
    print("Val docs: ",len(val_docs))


    with nlp.select_pipes(enable=["ner"]):
        optimizer=nlp.resume_training()

    best_f1=0.256
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

        batches=minibatch(train_examples,size=2)

        for batch in batches:
            nlp.update(batch,sgd=optimizer,drop=DROPOUT,losses=losses)
        
        f1,precision,recall=evaluate(nlp,val_docs)
        print(f"""
              Epoch {epoch+1+19}
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