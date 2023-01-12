import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# df = px.data.gapminder()

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
    # fig = go.Figure()
    # fig.add_trace(go.Histogram(x=l, name="count", texttemplate="%{x}"))
    return fig
