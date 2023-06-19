import streamlit as st
import pandas as pd
from io import BytesIO

from src.models.spacy_ner_model import SpacyModel
from src.utils.work_with_df import DataFrameHandler
from src.utils.visualization import get_hist_popular_entities,\
    get_entities_distr, get_entities_timeseries, get_entities_correlation
from src.web.css_code import file_uploader_css


class App:
    def __init__(self):
        self.nlp_model = SpacyModel()

    @staticmethod
    @st.cache_resource(max_entries=1, show_spinner=False)
    def get_entities_df(_nlp_model, news_df: pd.DataFrame, texts_amount: int, timeseries: bool):
        my_bar = st.progress(0.0)
        load_text = st.empty()
        load_text.write('Анализ сущностей в датасете...')
        total_df = pd.DataFrame()
        if timeseries:
            for idx, date, text_to_analyze in news_df.iloc[:, :2].itertuples():
                entities_df = _nlp_model.get_entities_df(text_to_analyze)
                if not entities_df.empty:
                    entities_df['номер текста'] = idx
                    entities_df['дата текста'] = date
                    total_df = pd.concat([total_df, entities_df])
                my_bar.progress(idx / texts_amount)
        else:
            for idx, text_to_analyze in news_df.iloc[:, :2].itertuples():
                entities_df = _nlp_model.get_entities_df(text_to_analyze)
                if not entities_df.empty:
                    entities_df['номер текста'] = idx
                    total_df = pd.concat([total_df, entities_df])
                my_bar.progress(idx / texts_amount)
        my_bar.empty()
        load_text.empty()
        total_df = total_df.reset_index(drop=True)
        st.markdown('---')
        st.markdown('### Результаты поиска именованных сущностей')
        st.write(f"Количество найденных сущностей: **{total_df.shape[0]}**")
        st.write(f"Количество уникальных сущностей: **{total_df['именованная сущность (норм.)'].nunique()}**")
        return total_df

    def _analyze_single_text(self):
        with st.form("text_to_analyze_form"):
            text_to_analyze = st.text_area(
                label='Введите ниже текст, который нужно проанализировать',
                value='Брат короля Саудовской Аравии критикует ближневосточный'
                            ' план президента США Джорджа Буша',
            )
            submitted = st.form_submit_button("Запуск анализа!")
            st.markdown(' ')
        if submitted:
            with st.spinner("Анализ текста..."):
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
        st.markdown('_Файл должен содержать лишь одну колонку с текстами_')
        st.markdown(file_uploader_css, unsafe_allow_html=True)
        uploaded_dataset = st.file_uploader(label='', type=['csv', 'txt'], key='upload_texts_only')
        load_example_dataset = st.button(label='Загрузить демо-набор', key='demo_texts_only')
        if load_example_dataset:
            uploaded_dataset = './data/processed/ria_news_jan_small.csv'
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
                total_df = self.get_entities_df(self.nlp_model,
                                                news_df,
                                                texts_amount,
                                                timeseries=False)
                st.write(total_df)
                st.markdown(' ')
                st.markdown('#### Визуализация')

                st.plotly_chart(
                    get_entities_distr(total_df),
                    theme="streamlit",
                    use_container_width=True
                )
                st.plotly_chart(
                    get_hist_popular_entities(total_df),
                    theme="streamlit",
                    use_container_width=True
                )

                st.markdown(' ')
                st.download_button(
                    label="Скачать таблицу с сущностями в формате .csv",
                    data=total_df.to_csv().encode('utf-8'),
                    file_name='entities_data.csv',
                    key='csv_texts_only'
                )
                st.download_button(
                    label="Скачать таблицу с сущностями в формате .xlsx",
                    data=DataFrameHandler.convert_df_to_excel(total_df),
                    file_name='entities_data.xlsx',
                    key='xlsx_texts_only'
                )
            else:
                st.warning('В загруженном наборе тексты не обнаружены!')

    def _analyze_dataset_with_date(self):
        st.markdown(' ')
        st.markdown('### **Загрузите файл с текстами в поле ниже**')
        st.markdown('_Файл должен содержать две колонки: с датами и текстами_')
        st.markdown(file_uploader_css, unsafe_allow_html=True)
        uploaded_dataset = st.file_uploader(label='', type=['csv', 'txt'], key='upload_texts_with_date')
        load_example_dataset = st.button(label='Загрузить демо-набор', key='demo_texts_with_date')
        if load_example_dataset:
            uploaded_dataset = './data/processed/ria_news_jan_small_dates.csv'
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
                total_df = self.get_entities_df(self.nlp_model,
                                                news_df,
                                                texts_amount,
                                                timeseries=True)
                st.write(total_df)
                st.markdown(' ')
                st.markdown('#### Визуализация')

                st.plotly_chart(
                    get_entities_distr(total_df),
                    theme="streamlit",
                    use_container_width=True
                )
                st.plotly_chart(
                    get_hist_popular_entities(total_df),
                    theme="streamlit",
                    use_container_width=True
                )
                st.plotly_chart(
                    get_entities_timeseries(total_df),
                    theme="streamlit",
                    use_container_width=True
                )
                st.plotly_chart(
                    get_entities_correlation(total_df),
                    theme="streamlit",
                    use_container_width=True
                )

                st.markdown(' ')
                st.download_button(
                    label="Скачать таблицу с сущностями в формате .csv",
                    data=total_df.to_csv().encode('utf-8'),
                    file_name='entities_data.csv',
                    key='csv_texts_only'
                )
                st.download_button(
                    label="Скачать таблицу с сущностями в формате .xlsx",
                    data=DataFrameHandler.convert_df_to_excel(total_df),
                    file_name='entities_data.xlsx',
                    key='xlsx_texts_only'
                )
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
        with st.expander("_О приложении 'News NER'_"):
            st.markdown("""
            Данное веб-приложение позволяет анализировать новостные тексты на наличие
            в них именованных сущностей.

            **Именованная сущность (Named Entity)** ⸺ это слово или словосочетание из текста, 
            обозначающее предмет или явление, которое можно классифицировать в одну из 
            заранее определённых категорий, таких как, например, имена людей,
            местоположения и названия организаций.

            С использованием модели нейронной сети в заданном тексте или наборе текстов будет
            производиться распознавание именованных сущностей, которые можно использовать
             в первичной аналитике данных.
            """)
        st.markdown(
            """
            Для распознавания доступны следующие именованные сущности:
            - **МЕС** ⸺ Местоположение
            - **ОРГ** ⸺ Организация
            - **ЛИЧ** ⸺ Личность
            """
        )
        single_text_block, many_texts_block, many_texts_with_date_block = st.tabs(
            ["Обработать новость", "Обработать набор новостей", "Обработать хронологию новостей"]
        )

        if 'texts_block' not in st.session_state:
            st.session_state.texts_block = None

        with single_text_block:
            self._analyze_single_text()
        with many_texts_block:
            self._analyze_dataset()
        with many_texts_with_date_block:
            self._analyze_dataset_with_date()
