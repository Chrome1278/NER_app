import pandas as pd
import os
import json
from tqdm import tqdm
import spacy
from spacy.tokens import DocBin
import re

json_name = 'labelled_annotations_val'


def trim_entity_spans(data: list) -> list:
    """Removes leading and trailing white spaces from entity spans.

    Args:
        data (list): The data to be cleaned in spaCy JSON format.

    Returns:
        list: The cleaned data.
    """
    invalid_span_tokens = re.compile(r'\s')

    cleaned_data = []
    for text, annotations in data:
        entities = annotations['entities']
        valid_entities = []
        for start, end, label in entities:
            valid_start = start
            valid_end = end
            while valid_start < len(text) and invalid_span_tokens.match(
                    text[valid_start]):
                valid_start += 1
            while valid_end > 1 and invalid_span_tokens.match(
                    text[valid_end - 1]):
                valid_end -= 1
            valid_entities.append([valid_start, valid_end, label])
        cleaned_data.append([text, {'entities': valid_entities}])

    return cleaned_data


with open(f'./data/annotations/{json_name}.json', 'r', encoding='utf8') as f:
    TRAIN_DATA = json.load(f)

train_data = TRAIN_DATA['annotations']
train_data = [tuple(i) for i in train_data]
train_data = trim_entity_spans(train_data)

# nlp = spacy.blank("ru") # load a new spacy model
nlp = spacy.load("ru_core_news_md")  # load other spacy model
db = DocBin()  # create a DocBin object

for text, annot in tqdm(train_data):  # data in previous format
    doc = nlp.make_doc(text)  # create doc object from text
    ents = []
    if annot["entities"] is None:
        continue
    for start, end, label in annot["entities"]:  # add character indexes
        span = doc.char_span(start, end, label=label, alignment_mode="contract")
        if span is None:
            continue
        else:
            ents.append(span)
    doc.ents = ents  # label the text with the ents
    db.add(doc)

db.to_disk(f"./data/annotations/{json_name}.spacy")  # save the docbin object
