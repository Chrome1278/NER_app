from nerus import load_nerus
from itertools import islice
import json

ner_docs = load_nerus('./data/raw/nerus_lenta.conllu.gz')
ner_classes = ["LOC", "ORG", "PER"]


def save_annotations(docs, docs_num, classes):
    for mode in ['train', 'val']:
        if mode == 'train':
            docs_list = list(islice(docs, docs_num))[:-2000]
            mode_in_file = ''
        else:
            docs_list = list(islice(docs, docs_num))[-2000:]
            mode_in_file = '_val'
        annotations = []
        annotations_dict = {}
        for doc in docs_list:  # docs
            ner_text = doc.ner.text
            ner_spans = doc.ner.spans
            entities_list = []
            for span in ner_spans:
                ent_start = span.start
                ent_stop = span.stop
                ent_type = span.type

                entities_list.append([ent_start, ent_stop, ent_type])
            entities_dict = {'entities': entities_list}

            annotations.append([f"\"{ner_text}\"\r", entities_dict])

        annotations_dict['classes'] = classes
        annotations_dict['annotations'] = annotations

        with open(f'./data/annotations/labelled_annotations{mode_in_file}.json',
                  'w',
                  encoding='utf8') as file:
            json.dump(annotations_dict, file, ensure_ascii=False)


save_annotations(docs=ner_docs, docs_num=22000, classes=ner_classes)






