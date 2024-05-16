import pandas as pd
import datetime
import logging
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
import dotenv
import os
from pprint import pprint
import json

DATA_DIR = "../data/raw/"
os.makedirs(DATA_DIR, exist_ok=True)

def initialize_project(stock_symbol: str):
    dotenv.load_dotenv('../.env')

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey={os.getenv("AV_API_KEY")}'
    r = requests.get(url)
    data = r.json()
    
    with open(f'{DATA_DIR}stock_data.json', 'w') as file:
        json.dump(data, file)
    
    df = pd.DataFrame(data.get("Time Series (5min)"))
    df_transposed = df.T
    df_transposed.columns = ['open', 'high', 'low', 'close', 'volume']
    df_transposed[['open', 'high', 'low', 'close', 'volume']] = df_transposed[['open', 'high', 'low', 'close', 'volume']].astype(float)
    
    return df_transposed

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    return data