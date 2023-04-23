import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


def get_hist_popular_entities(df):
    df = df.groupby(['lemma_', 'label_']).size().reset_index(name='counts')
    df = df.sort_values(by=['counts'], ascending=True)[-10:]
    fig = px.histogram(
        df,
        x="counts",
        y="lemma_",
        color="label_",
        text_auto=True,
        title="Топ 10 найденных сущностей",
        height=600,
    )
    fig.update_layout(xaxis_title="Количество нахождений")
    fig.update_layout(yaxis_title="Леммы слов")
    fig.update_layout(font=dict(size=16))
    fig.update_layout(bargap=0.2)
    return fig


def get_entities_distr(df):
    df = df.groupby(['label_']).size().reset_index(name='counts')
    df = df.sort_values(by=['counts'], ascending=True)  # [-10:]
    fig = px.histogram(
        df,
        y="counts",
        x="label_",
        color="label_",
        text_auto=True,
        title="Количество нахождений по каждой из сущностей",
        height=500,
    )
    fig.update_layout(xaxis_title="Виды сущностей")
    fig.update_layout(yaxis_title="Количество нахождений")
    fig.update_layout(font=dict(size=16))
    fig.update_layout(bargap=0.2)
    return fig


def get_entities_timeseries(df):
    df = df.groupby(['lemma_', 'text_date']).size().reset_index(name='counts')
    df = df.sort_values(by=['text_date'], ascending=True)  # [-10:]

    top_lemmas_df = df.groupby(['lemma_']).size().reset_index(name='counts') \
        .sort_values(by=['counts'], ascending=True)[-10:]
    df = df[df.lemma_.isin(top_lemmas_df.lemma_)]

    fig = px.line(
        df,
        y="counts",
        x="text_date",
        color="lemma_",
        title="Временной ряд по топ-10 найденным сущностям",
        height=600,
    )
    fig.update_layout(xaxis_title="Виды сущностей")
    fig.update_layout(yaxis_title="Даты")
    fig.update_layout(font=dict(size=16))
    return fig


def get_entities_correlation(df):
    df = df.groupby(['lemma_', 'text_date']).size().reset_index(name='counts')
    df = df.sort_values(by=['text_date'], ascending=True)  # [-10:]

    top_lemmas_df = df.groupby(['lemma_']).size().reset_index(name='counts') \
        .sort_values(by=['counts'], ascending=True)[-10:]
    df = df[df.lemma_.isin(top_lemmas_df.lemma_)]

    df_pivot = df.pivot_table(
        index='text_date', columns='lemma_', values='counts'
    ).reset_index(drop=True)
    df_pivot = df_pivot.rename_axis(None, axis=1)

    corr_matrix = df_pivot.corr()
    fig = px.imshow(
        corr_matrix,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        title="Корреляция между топ-10 найденными сущностями",
        height=700,
    )
    fig.update_layout(font=dict(size=16))
    return fig

