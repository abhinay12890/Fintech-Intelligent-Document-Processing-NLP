import json
import spacy
from spacy.tokens import DocBin
from pathlib import Path
from spacy.util import filter_spans

import re

LABEL_MAP = {

    # Parties
    "PARTIES": "PARTY",
    "AFFILIATE_LICENSE_LICENSEE": "PARTY",
    "AFFILIATE_LICENSE_LICENSOR": "PARTY",
    "THIRD_PARTY_BENEFICIARY": "PARTY",

    # Dates
    "AGREEMENT_DATE": "CONTRACT_DATE",
    "EFFECTIVE_DATE": "CONTRACT_DATE",
    "EXPIRATION_DATE": "CONTRACT_DATE",

    # Liability / Financial
    "CAP_ON_LIABILITY": "LIABILITY",
    "UNCAPPED_LIABILITY": "LIABILITY",
    "LIQUIDATED_DAMAGES": "LIABILITY",

    "REVENUE_PROFIT_SHARING": "PAYMENT_TERM",
    "MINIMUM_COMMITMENT": "PAYMENT_TERM",
    "PRICE_RESTRICTIONS": "PAYMENT_TERM",

    # License / IP
    "LICENSE_GRANT": "LICENSE_TERM",
    "IRREVOCABLE_OR_PERPETUAL_LICENSE": "LICENSE_TERM",
    "NON_TRANSFERABLE_LICENSE": "LICENSE_TERM",
    "UNLIMITED_ALL_YOU_CAN_EAT_LICENSE": "LICENSE_TERM",
    "VOLUME_RESTRICTION":"LICENSE_TERM",

    "IP_OWNERSHIP_ASSIGNMENT": "IP_OWNERSHIP",
    "JOINT_IP_OWNERSHIP": "IP_OWNERSHIP",

    # Restrictions
    "NON_COMPETE": "RESTRICTION",
    "NON_DISPARAGEMENT": "RESTRICTION",
    "NO_SOLICIT_OF_CUSTOMERS": "RESTRICTION",
    "NO_SOLICIT_OF_EMPLOYEES": "RESTRICTION",
    "EXCLUSIVITY": "RESTRICTION",
    "COMPETITIVE_RESTRICTION_EXCEPTION": "RESTRICTION",
    "ROFR_ROFO_ROFN":"RESTRICTION",
    "CHANGE_OF_CONTROL":"RESTRICTION",

    # Termination / Legal
    "TERMINATION_FOR_CONVENIENCE": "TERMINATION",
    "POST_TERMINATION_SERVICES": "TERMINATION",
    "NOTICE_PERIOD_TO_TERMINATE_RENEWAL": "TERMINATION",
    "RENEWAL_TERM": "TERMINATION",

    "GOVERNING_LAW": "LEGAL",
    "MOST_FAVORED_NATION":"LEGAL",
    "COVENANT_NOT_TO_SUE":"LEGAL",
    "SOURCE_CODE_ESCROW":"LEGAL",

}


def extract_label(question):
    match = re.search(r'"([^"]+)"', question)
    if not match:
        return None

    raw_label = match.group(1).upper().replace(" ", "_").replace("/","_").replace("-","_")

    GENERIC_LABELS = {"CARDINAL","ORDINAL","WORK_OF_ART","FAC"}
    if raw_label in GENERIC_LABELS:
        return None
    else:
        return LABEL_MAP.get(raw_label) # Merge labels



def convert_cuad_to_spacy(cuad_path, output_path):
    nlp = spacy.blank("en")
    doc_bin = DocBin()

    with open(cuad_path, "r") as f:
        cuad = json.load(f)

    dropped_spans = 0
    kept_spans = 0
    docs_with_entities = 0


    for doc in cuad["data"]:
        for para in doc["paragraphs"]:
            text = para["context"]
            spacy_doc = nlp.make_doc(text)
            ents = []

            for qa in para["qas"]:
                if qa.get("is_impossible", False):
                    continue

                label = extract_label(qa["question"])
                if not label:
                    continue

                for ans in qa["answers"]:
                    text_ans = ans["text"].strip()
                    start = text.find(text_ans, ans["answer_start"])
                    if start == -1:
                          continue
                    end = start + len(text_ans)

                    span = spacy_doc.char_span(
                         start, end,label=label, alignment_mode="contract")
                    #  HARD SPAN VALIDATION
                    if ( span is None  or span.start >= span.end  or span.text != span.text.strip()
                        or "\n" in span.text or span[-1].is_punct  or len(span) > 80):
                         dropped_spans += 1
                         continue
                    ents.append(span)
                    kept_spans += 1


            if ents:
                before=len(ents)
                ents=list(set(ents))
                ents=filter_spans(sorted(ents,key=lambda x: (x.start,-x.end)))
                spacy_doc.ents=ents
                doc_bin.add(spacy_doc)
                docs_with_entities += 1
                after=len(ents)
                dropped_spans+=(before-after)

    print("Kept spans:", kept_spans)
    print("Dropped spans:", dropped_spans)
    print("Docs with entities:", docs_with_entities)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    doc_bin.to_disk(output_path)


if __name__ == "__main__":
    convert_cuad_to_spacy(
        "CUADv1.json",
        "data/ner/train.spacy"
    )
