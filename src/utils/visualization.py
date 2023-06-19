from datetime import datetime

import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import locale
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

def get_hist_popular_entities(df):
    df = df.groupby(['именованная сущность (норм.)', 'категория']).size().reset_index(name='counts')
    df = df.sort_values(by=['counts'], ascending=True)[-10:]
    fig = px.histogram(
        df,
        x="counts",
        y="именованная сущность (норм.)",
        color="категория",
        text_auto=True,
        title="Топ 10 найденных сущностей",
        height=450,
    )
    fig.update_layout(
        # title="Plot Title",
        xaxis_title="Количество нахождений",
        yaxis_title="Именованные сущности",
        legend_title="Категории",
        title_font=dict(
            size=20,
            color="black"
        ),
        legend_font=dict(
            size=16,
            color="black"
        ),
        legend_title_font=dict(
            size=18,
            color="black"
        ),
        legend_grouptitlefont=dict(
            size=18,
            color="black"
        ),
        font=dict(
            size=16,
        ),
        bargap=0.2,
    )
    return fig


def get_entities_distr(df):
    df = df.groupby(['категория']).size().reset_index(name='counts')
    df = df.sort_values(by=['counts'], ascending=True)  # [-10:]
    fig = px.histogram(
        df,
        y="counts",
        x="категория",
        color="категория",
        text_auto=True,
        title="Количество нахождений по каждой из категории именованных сущностей",
        height=450,
    )
    fig.update_layout(
        xaxis_title="Категории сущностей",
        yaxis_title="Количество нахождений",
        legend_title="Категории",
        title_font=dict(
            size=20,
            color="black"
        ),
        legend_font=dict(
            size=16,
            color="black"
        ),
        legend_title_font=dict(
            size=18,
            color="black"
        ),
        legend_grouptitlefont=dict(
            size=18,
            color="black"
        ),
        font=dict(
            size=16,
        ),
        bargap=0.2,
    )
    return fig


def get_entities_timeseries(df):
    df = df.groupby(['именованная сущность (норм.)', 'дата текста']).size().reset_index(name='counts')
    df = df.sort_values(by=['дата текста'], ascending=True)  # [-10:]

    top_lemmas_df = df.groupby(['именованная сущность (норм.)']).size().reset_index(name='counts') \
                        .sort_values(by=['counts'], ascending=True)[-10:]
    df = df[df['именованная сущность (норм.)'].isin(top_lemmas_df['именованная сущность (норм.)'])]

    fig = px.line(
        df,
        y="counts",
        x="дата текста",
        color="именованная сущность (норм.)",
        title="Временной ряд по топ-10 найденным сущностям",
        height=450,
    )

    ticktext = [datetime.strptime(elem, "%Y-%m-%d").strftime('%d-%b-%Y')
                for elem in df['дата текста']]
    fig.update_xaxes(tickformat='%d-%m-%y')
    fig.update_xaxes(tickvals=df['дата текста'])
    fig.update_xaxes(ticktext=ticktext)

    fig.update_layout(
        yaxis_title="Количество упоминаний",
        xaxis_title="Даты",
        legend_title="Именованные сущности",
        title_font=dict(
            size=20,
            color="black"
        ),
        legend_font=dict(
            size=16,
            color="black"
        ),
        legend_title_font=dict(
            size=18,
            color="black"
        ),
        legend_grouptitlefont=dict(
            size=18,
            color="black"
        ),
        font=dict(
            size=16,
        ),
        bargap=0.2,
    )
    return fig


def get_entities_correlation(df):
    df = df.groupby(['именованная сущность (норм.)', 'дата текста']).size().reset_index(name='counts')
    df = df.sort_values(by=['дата текста'], ascending=True)  # [-10:]

    top_lemmas_df = df.groupby(['именованная сущность (норм.)']).size().reset_index(name='counts') \
                        .sort_values(by=['counts'], ascending=True)[-10:]
    df = df[df['именованная сущность (норм.)'].isin(top_lemmas_df['именованная сущность (норм.)'])]

    df_pivot = df.pivot_table(
        index='дата текста', columns='именованная сущность (норм.)', values='counts'
    ).reset_index(drop=True)
    df_pivot = df_pivot.rename_axis(None, axis=1)
    df_pivot = df_pivot.fillna(0)
    print(df_pivot)
    corr_matrix = df_pivot.corr('spearman')
    print()
    print(corr_matrix)
    fig = px.imshow(
        corr_matrix,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        zmin=-1,
        zmax=1,
        title="Корреляция между топ-10 найденными сущностями",
        height=500,
    )
    fig.update_layout(font=dict(size=16))
    return fig
