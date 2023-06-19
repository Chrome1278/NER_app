import spacy
from spacy import displacy, Language
import pandas as pd
import pathlib

from spacy.tokens import Doc, Token, Span


class SpacyModel:
    def __init__(self):
        path = pathlib.Path(__file__).parent / 'model_ner/'
        self.nlp = spacy.load(path)
        self.nlp.add_pipe('set_custom_ner_labels', after="ner")
        ner_labels = {
            "PER": "ЛИЧ",
            "ORG": "ОРГ",
            "LOC": "МЕС"
        }
        Doc.set_extension('ner_labels', force=True, default=ner_labels)

    @staticmethod
    @Language.component("set_custom_ner_labels")
    def set_custom_ner_labels(doc):
        ner_labels = {
            "PER": "ЛИЧ",
            "ORG": "ОРГ",
            "LOC": "МЕС"
        }
        new_ents = []
        seen_tokens = set()
        for ent in doc.ents:
            if ent.start in seen_tokens:
                continue
            if ent.label_ in ner_labels:
                new_ent = Span(ent.doc, ent.start, ent.end, label=ner_labels[ent.label_])
                new_ents.append(new_ent)
                for token in new_ent:
                    seen_tokens.add(token.i)
        doc.ents = new_ents
        return doc

    def get_output_entities(self, text: str):
        nlp_gen = self.nlp.pipe([text], disable=["tagger", "parser"])
        entities = next(nlp_gen).ents
        output = [(ent.text, ent.label_) for ent in entities]
        return output

    def get_res(self, text: str):
        doc = self.nlp(text)
        attrs = [
            "text",
            "lemma_",
            "label_",
            "start", "end",
            "start_char",
            "end_char",
        ]
        data = [
            [str(getattr(ent, attr)) for attr in attrs]
            for ent in doc.ents
        ]
        print(data)

    def get_visualized_output(self, text: str):
        doc = self.nlp(text)
        colors = {"ЛИЧ": "#FFB266", "ОРГ": "#66FF66", "МЕС": "#66FFFF"}
        options = {"ents": ['ЛИЧ', 'МЕС', "ОРГ"], "colors": colors}
        ent_svg = displacy.render(
            doc, style='ent', options=options, minify=True, jupyter=False, page=True
        )
        print(ent_svg)
        return ent_svg

    def get_entities_df(self, text: str) -> pd.DataFrame:
        doc = self.nlp(text)
        doc._.ner_labels = self.ner_labels

        attrs = [
            "text",
            "lemma_",
            "label_",
            "start", "end",
            "start_char",
            "end_char",
        ]
        attrs_ru = [
            "именованная сущность",
            "именованная сущность (норм.)",
            "категория",
            "номер перв. слова",
            "номер посл. слова",
            "номер перв. символа",
            "номер послед. символа",
        ]
        data = [
            [str(getattr(ent, attr)) for attr in attrs]
            for ent in doc.ents
        ]
        df = pd.DataFrame(data, columns=attrs_ru)
        df.loc[
            df['именованная сущность'].str.lower() == df['именованная сущность (норм.)'].str.lower(),
            'именованная сущность (норм.)'
        ] = df['именованная сущность']
        df['именованная сущность (норм.)'] = df['именованная сущность (норм.)'].apply(
            lambda entity: ' '.join(
                [word[:1].upper() + word[1:] if len(word) > 1 else word for word in entity.split()]
            )
        )
        return df
