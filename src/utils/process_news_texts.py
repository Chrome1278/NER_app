import pandas as pd

texts_df = pd.read_csv('./data/raw/lenta.csv')
texts_df = texts_df[texts_df['card-full-news__title'].str.len() > 5]
texts_df = texts_df.drop_duplicates(subset=['card-full-news__title'])

texts_df[['card-full-news__title']].to_csv(
    r'./data/processed/demo_news.txt', header=None, index=None, sep=' ', mode='w'
)
texts_df[['card-full-news__title']][:10].to_csv(
    r'./data/processed/header_news_small.txt', header=None, index=None, sep=' ', mode='w'
)

print(texts_df.shape)
