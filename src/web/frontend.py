import streamlit as st
import pandas as pd
from io import BytesIO
from src.models.spacy_ner_model import SpacyModel


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
                        data=self.df_to_excel(entities_df),
                        file_name='entities_df.xlsx',
                    )
                    st.markdown(' ')
                else:
                    st.warning('В введённом тексте не найдено каких-либо сущностей!')

    @staticmethod
    def df_to_excel(df):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        format1 = workbook.add_format({'num_format': '0.00'})
        worksheet.set_column('A:A', None, format1)
        writer.save()
        processed_data = output.getvalue()
        return processed_data

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
