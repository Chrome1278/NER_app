import spacy
from spacy import displacy
import pandas as pd


class SpacyModel:
    def __init__(self):
        self.nlp = spacy.load('ru_core_news_md')

        # new_vocab = ['PRO']
        # self.nlp = spacy.load('ru_core_news_md')
        # print(self.nlp.vocab.strings)
        # for item in new_vocab:
        #     self.nlp.vocab.strings.add(item)
        # extended_nlp = spacy.load('./src/models/tuning_models_news/model-best')
        # print(extended_nlp.get_pipe('ner').labels)
        # print(self.nlp.get_pipe("ner").labels)
        # self.nlp.add_pipe(
        #     'ner',
        #     name="ner_extended",
        #     source=extended_nlp,
        #     after="ner",
        # )
        # print(self.nlp.get_pipe("ner").labels)
        # self.extended_nlp = spacy.load('./src/models/tuning_models/model-best')
        # self.nlp = spacy.load('ru_core_news_md')
        # self.nlp.replace_listeners("tok2vec", "ner", ["model.tok2vec"])
        #
        # self.extended_nlp.add_pipe(
        #     "ner",
        #     name="ner_tuned",
        #     source=self.nlp,
        #     after="ner",
        # )

    def get_output_entities(self, text: str):
        nlp_gen = self.nlp.pipe([text], disable=["tagger", "parser"])
        entities = next(nlp_gen).ents
        output = [(ent.text, ent.label_) for ent in entities]
        return output

    def get_visualized_output(self, text: str):
        doc = self.nlp(text)
        ent_svg = displacy.render(doc, style='ent', minify=True, jupyter=False, page=True)
        return ent_svg

    def get_entities_df(self, text: str) -> pd.DataFrame:
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
        df = pd.DataFrame(data, columns=attrs)
        return df
