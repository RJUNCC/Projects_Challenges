#%%
import requests
import json
import pandas as pd
import numpy as np
from newsapi import NewsApiClient
import nltk
nltk.downloader.download('vader_lexicon')

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os
from dotenv import load_dotenv
# from pprint import pprint
import logging
import streamlit as st
# from textblob import TextBlob
from functions import *
st.set_page_config(layout='wide')
# %%
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# %%
load_dotenv("../.env")

# %%
# client = NewsApiClient(api_key=os.getenv("NEWSAPI_KEY"))
# client = NewsApiClient(api_key="4a107bac530044a4a6689d38744dcc65")
client = NewsApiClient(api_key=st.secrets['NEWSAPI_KEY'])


analyzer = SentimentIntensityAnalyzer()
bitcoin_sentiments = []

#%%
sentiment_count = {
    "Positive":0,
    "Neutral":0,
    "Negative":0
}


st.title("News App")
topic = st.text_input("Input topic")
try:
    language = st.sidebar.text_input('Country code')
    st.sidebar.markdown("Possible options: \n ar, de, en, es, fr, he, it, nl, no, pt, ru, sv, ud, zh")
    language = language.lower()

    if language == "":
        language = "en"
except ValueError as e:
    print("Error: Not a valid language")

if st.button("Search"):
    try:
        headlines = client.get_everything(q=topic, language=language, page_size=100, sort_by='relevancy')
        st.header(str(topic).title())
        index = 0
    except requests.exceptions.RequestException as e:
        print("Error making request: ", e)
    for article in headlines['articles']: 
        try:
            text      = article['content']
            date      = article['publishedAt'][:10]
            sentiment = analyzer.polarity_scores(text)
            compound  = sentiment['compound']
            pos       = sentiment['pos']
            neu       = sentiment['neu']
            neg       = sentiment['neg']

            if pos > neu and pos > neg:
                sentiment_count['Positive'] += 1
            elif neu > pos and neu > neg:
                sentiment_count['Neutral'] += 1
            else:
                sentiment_count['Negative'] += 1

            bitcoin_sentiments.append({
                'text':text,
                'date':date,
                'compound':compound,
                'positive':pos,
                'negative':neg,
                'neutral':neu
            })         
        
        except AttributeError:
            pass

        # st.markdown(
        #     """
        #     <style>
        #     .reportview-container .main .block-container {
        #         max-width: 3000px;
        #     }
        #     </style>
        #     """,
        #     unsafe_allow_html=True
        # )

        with st.container(border=True):
            if article['title'] == "[Removed]":
                continue
            if article['description'] is None:
                continue
            col1, col2, col3= st.columns(3)

            col1.markdown("#### **Description**")
            col1.markdown(f"### [{article['title']}]({article['url']})")
            col1.write(article['description'].replace("$", ""))

            col2.markdown("#### **Other Info**")
            col2.markdown("#### Pubslished at: " + f"{article['publishedAt'][:16]}")
            col2.markdown('#### Author: ' + str(article['author']))
            col2.markdown("#### ")

            most_common_noun, count = get_most_common_noun_with_count(article['description'])
            if count > 1:
                col2.markdown(f"#### Most common noun, \"{most_common_noun}\", shows up {count} times.")
            else:
                col2.markdown(f"#### No most common noun found.")
            
            


            col3.markdown("#### **Sentiment**")
            col3.metric(label="positive", value=bitcoin_sentiments[index]['positive'])
            col3.metric(label="neutral", value=bitcoin_sentiments[index]['neutral'])
            col3.metric(label="negative", value=bitcoin_sentiments[index]['negative'])

            # col4.markdown(f"!['Image']({article['urlToImage']})")
        index = index + 1
    
    st.sidebar.metric(label="Common Sentiment", value=max(sentiment_count, key=sentiment_count.get))

# %%
