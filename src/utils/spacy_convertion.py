import pandas as pd
import os
import json
from tqdm import tqdm
import spacy
from spacy.tokens import DocBin

json_name = 'annotations_new.json'  # annotations.json

with open(f'./data/annotations/{json_name}', 'r') as f:
    TRAIN_DATA = json.load(f)

train_data = TRAIN_DATA['annotations']
train_data = [tuple(i) for i in train_data]

# nlp = spacy.blank("ru") # load a new spacy model
nlp = spacy.load("ru_core_news_md")  # load other spacy model
db = DocBin()  # create a DocBin object

for text, annot in tqdm(train_data):  # data in previous format
    doc = nlp.make_doc(text)  # create doc object from text
    ents = []
    for start, end, label in annot["entities"]:  # add character indexes
        span = doc.char_span(start, end, label=label, alignment_mode="contract")
        if span is None:
            print("Skipping entity")
        else:
            ents.append(span)
    doc.ents = ents  # label the text with the ents
    db.add(doc)

db.to_disk(f"./data/annotations/{json_name}")  # save the docbin object
