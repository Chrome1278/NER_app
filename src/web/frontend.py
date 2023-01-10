import streamlit as st
import pandas as pd
from io import BytesIO

from src.models.spacy_ner_model import SpacyModel
from src.utils.work_with_df import DataFrameHandler


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
                    st.markdown(' ')
                    st.markdown(' ')
                    st.subheader('**Результат обработки:**')
                    entities_html_visualize = self.nlp_model.get_visualized_output(text_to_analyze)
                    st.markdown(entities_html_visualize, unsafe_allow_html=True)
                    st.markdown(' ')
                    st.markdown(' ')
                    st.markdown('*Таблица с найденными сущностями:*')
                    entities_df = self.nlp_model.get_entities_df(text_to_analyze)
                    st.dataframe(entities_df)
                    st.download_button(
                        label="Скачать таблицу с сущностями",
                        data=DataFrameHandler.convert_df_to_excel(entities_df),
                        file_name='entities_df.xlsx',
                    )
                    st.markdown(' ')
                else:
                    st.warning('В введённом тексте не найдено каких-либо сущностей!')

    def _analyze_dataset(self):
        st.markdown(' ')
        st.subheader('**Загрузите файл с текстами в поле ниже**')
        uploaded_dataset = st.file_uploader(label='', type=['csv', 'txt'])
        if uploaded_dataset is not None:
            news_df = pd.read_csv(uploaded_dataset)
            st.markdown(' ')
            st.write(f"Количество текстов, загруженных для анализа: **{news_df.shape[0]}**")
            st.markdown(' ')

            total_df = pd.DataFrame()
            for idx, text_to_analyze in news_df.iloc[:, :1].itertuples():
                output_entities = self.nlp_model.get_output_entities(text_to_analyze)
                if output_entities:
                    entities_df = self.nlp_model.get_entities_df(text_to_analyze)
                    entities_df['text_id'] = idx
                    total_df = pd.concat([total_df, entities_df])

            st.write(f"Количество найденных сущностей: **{total_df.shape[0]}**")
            st.write(f"Количество уникальных сущностей: **{total_df.text.nunique()}**")
            st.write(total_df)

    def __call__(self):
        st.session_state.lang = 'ru'
        st.set_page_config(
            page_title="News NER",
            page_icon=":globe_with_meridians:",
            layout="centered",
        )
        st.title('Распознование именованных сущностей в новостных текстах')
        st.markdown(
            """
            Выделяются следующие сущности:
            - **LOC** - Локация (улицы, города, страны)
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
            self._analyze_dataset()
