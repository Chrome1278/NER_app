import time
import sys

import streamlit as st

from src.model.test_model import predict

def run():

    st.set_page_config(
        page_title="News NER",
        page_icon=":globe_with_meridians:",
        layout="centered"
    )

    st.title('Hello!')

    one_text_block, text_df_block = st.tabs(["Обработать текст", "Обработать набор текстов"])

    with one_text_block:
        st.header("ONE TEXT")

        with st.form("text_to_analyze_form"):
            text_to_analyze = st.text_area(
                'Введите ниже текст, который нужно проанализировать',
            )

            # Every form must have a submit button.
            submitted = st.form_submit_button("Запуск анализа!")
            if submitted:
                with st.spinner("Анализ текста..."):
                    analyzed_text = predict(text_to_analyze)
                    pass
                st.success(f'Текст успешно обработан! Результат: {analyzed_text}')

        st.write("Outside the form")




    with text_df_block:
        st.header("MANY TEXT AS DATAFRAME")
        # st.file_uploader("Choose a file")



# items = st.text_area(
#             'Insert your food items here (separated by `,`): ',
#             pure_comma_separation(prompt_box, return_list=False),
#         )
#         items = pure_comma_separation(items, return_list=False)
#         entered_items = st.empty()
