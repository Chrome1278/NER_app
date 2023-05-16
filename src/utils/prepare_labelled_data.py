from nerus import load_nerus
from itertools import islice
import json
import conllu
from tqdm import tqdm

# download dataset from https://github.com/natasha/nerus
ner_docs = load_nerus('./data/raw/nerus_lenta.conllu.gz')
ner_classes = ["LOC", "ORG", "PER"]


def make_small_conllu(docs_num):
    conllu_path = './data/raw/nerus_lenta.conllu'
    # открываем исходный файл на чтение
    with open(conllu_path, "r", encoding="utf-8") as f:
        # открываем новый файл на запись
        with open("./data/raw/nerus_lenta_small.conllu", "w", encoding="utf-8") as out_file:
            # читаем файл построчно
            lines_count = 0
            for line in f:
                # парсим строку в формате .conll
                parsed_line = conllu.parser.parse_line(line)
                out_file.write(conllu. serialize([parsed_line]))
                lines_count += 1
                # записываем выбранные строки в новый .conll файл
                if lines_count == docs_num:
                    return


def save_annotations(docs, docs_num, val_num, file_name, classes):
    full_docs_list = list(islice(docs, docs_num))
    for mode in ['train', 'val']:
        if mode == 'train':
            docs_list = full_docs_list[:-val_num]
            mode_in_file = ''
        else:
            docs_list = full_docs_list[-val_num:]
            mode_in_file = '_val'
        annotations = []
        annotations_dict = {}
        for doc in tqdm(docs_list):  # docs
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

        with open(f'./data/annotations/{file_name}{mode_in_file}.json',
                  'w',
                  encoding='utf8') as file:
            json.dump(annotations_dict, file, ensure_ascii=False)


# save_annotations(docs=ner_docs,
#                  docs_num=50000,
#                  val_num=5000,
#                  file_name='labelled_annotations_large',
#                  classes=ner_classes)

# make_small_conllu(5)


