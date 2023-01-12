import streamlit as st
import pandas as pd
from io import BytesIO

from src.models.spacy_ner_model import SpacyModel
from src.utils.work_with_df import DataFrameHandler
from src.utils.visualization import get_hist_popular_entities
from src.web.css_code import file_uploader_css


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
                entities_df = self.nlp_model.get_entities_df(text_to_analyze)
                if not entities_df.empty:
                    st.markdown(' ')
                    st.markdown(' ')
                    st.subheader('**Результат обработки:**')
                    entities_html_visualize = self.nlp_model.get_visualized_output(text_to_analyze)
                    st.markdown(entities_html_visualize, unsafe_allow_html=True)
                    st.markdown('*Таблица с найденными сущностями:*')
                    st.dataframe(entities_df)
                    st.markdown(' ')
                    st.download_button(
                        label="Скачать таблицу с сущностями в формате .csv",
                        data=entities_df.to_csv().encode('utf-8'),
                        file_name='entities_data.csv'
                    )
                    st.download_button(
                        label="Скачать таблицу с сущностями в формате .xlsx",
                        data=DataFrameHandler.convert_df_to_excel(entities_df),
                        file_name='entities_data.xlsx',
                    )
                else:
                    st.warning('В введённом тексте не найдено каких-либо сущностей!')

    def _analyze_dataset(self):
        st.markdown(' ')
        st.markdown('### **Загрузите файл с текстами в поле ниже**')
        st.markdown(file_uploader_css, unsafe_allow_html=True)
        uploaded_dataset = st.file_uploader(label='', type=['csv', 'txt'])
        if uploaded_dataset is not None:
            news_df = pd.read_csv(uploaded_dataset)
            st.markdown(' ')
            st.write('*Загруженный датасет:*')
            st.write(news_df)
            texts_amount = news_df.shape[0]
            if texts_amount > 0:
                st.write(f"Количество текстов, загруженных для анализа: **{texts_amount}**")
                st.markdown(' ')
                st.markdown(' ')
                my_bar = st.progress(0.0)
                load_text = st.empty()
                load_text.write('Анализ сущностей в датасете...')
                total_df = pd.DataFrame()
                for idx, text_to_analyze in news_df.iloc[:, :1].itertuples():
                    entities_df = self.nlp_model.get_entities_df(text_to_analyze)
                    if not entities_df.empty:
                        entities_df['text_id'] = idx
                        total_df = pd.concat([total_df, entities_df])
                    my_bar.progress(idx/texts_amount)
                my_bar.empty()
                load_text.empty()
                st.markdown('---')
                st.markdown('### Результаты поиска именованных сущностей')
                st.write(f"Количество найденных сущностей: **{total_df.shape[0]}**")
                st.write(f"Количество уникальных сущностей: **{total_df.lemma_.nunique()}**")
                st.write(total_df)
                st.markdown(' ')
                st.markdown('#### Визуализация')
                st.plotly_chart(
                    get_hist_popular_entities(total_df),
                    theme="streamlit",
                    use_container_width=True)
            else:
                st.warning('В загруженном наборе тексты не обнаружены!')

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
