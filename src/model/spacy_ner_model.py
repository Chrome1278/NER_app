import spacy
from spacy import displacy


class SpacyModel:
    def __init__(self):
        self.nlp = spacy.load('ru_core_news_md')

    def get_output_entities(self, text):
        nlp_gen = self.nlp.pipe([text], disable=["tagger", "parser"])
        entities = next(nlp_gen).ents
        output = [(ent.text, ent.label_) for ent in entities]
        return output

    def get_visualized_output(self, text):
        doc = self.nlp(text)
        ent_svg = displacy.render(doc, style='ent', minify=True, jupyter=False)
        return ent_svg

