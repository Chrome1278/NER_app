import streamlit as st

from src.model.spacy_ner_model import SpacyModel


class App:
    def __init__(self):
        self.nlp_model = SpacyModel()

    def _analyze_single_text(self):
        with st.form("text_to_analyze_form"):
            text_to_analyze = st.text_area(
                'Введите ниже текст, который нужно проанализировать',
            )
            submitted = st.form_submit_button("Запуск анализа!")
            st.markdown(' ')
            if submitted:
                with st.spinner("Анализ текста..."):
                    # todo: Делать ли предобработку текста ?
                    output_entities = self.nlp_model.get_output_entities(text_to_analyze)
                    if output_entities:
                        st.subheader('**Результат обработки:**')
                        entities_html = self.nlp_model.get_visualized_output(text_to_analyze)
                        st.markdown(entities_html, unsafe_allow_html=True)
                        st.markdown(' ')
                    else:
                        st.warning('Введённый текст нельзя обработать! '
                                   'Возможно, текст слишком короткий.')
            st.empty()

    def __call__(self):
        st.set_page_config(
            page_title="News NER",
            page_icon=":globe_with_meridians:",
            layout="centered",

        )
        st.title('Распознование именованных сущностей в новостных текстах')
        st.markdown(
            """
            Выделяются следующие сущности:
            - **LOC** - Локация
            - **ORG** - Оганизация
            - **PER** - Личность
            """
        )
        single_text_block, many_texts_block = st.tabs(
            ["Обработать текст", "Обработать набор текстов"]
        )
        with single_text_block:
            self._analyze_single_text()
        with many_texts_block:
            st.info('Находится в разработке!')
