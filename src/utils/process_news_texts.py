import pandas as pd

texts_df = pd.read_csv('./data/raw/lenta.csv')
texts_df = texts_df[texts_df['card-full-news__title'].str.len() > 10]
texts_df = texts_df.drop_duplicates(subset=['card-full-news__title'])

texts_df['card-full-news__title'].to_csv(
    r'./data/processed/header_news.txt', header=None, index=None, sep=' ', mode='a'
)

texts_df['card-full-news__title'][:10].to_csv(
    r'./data/processed/header_news_small.txt', header=None, index=None, sep=' ', mode='a'
)

print(texts_df.shape)
