import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset
from torch.utils.data import DataLoader

import yfinance as yf

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

from alpha_vantage.timeseries import TimeSeries 
import dotenv
import os

print("All libraries loaded")

class Config:
    # load environment variables
    dotenv.load_dotenv('../.env')

    # constructor
    def __init__(self, symbol):
        self.symbol = symbol

        self.config = {
            "alpha_vantage": {
                "key": os.getenv("AV_API_KEY"), # you can use the demo API key for this project, but please make sure to get your own API key at https://www.alphavantage.co/support/#api-key
                "symbol":self.symbol,
                "outputsize": "full",
                "key_adjusted_close": "5. adjusted close",
            },
            "yf": {
                "symbol": self.symbol
            },
            "data": {
                "window_size": 20,
                "train_split_size": 0.80,
            }, 
            "plots": {
                "xticks_interval": 90, # show a date every 90 days
                "color_actual": "#001f3f",
                "color_train": "#3D9970",
                "color_val": "#0074D9",
                "color_pred_train": "#3D9970",
                "color_pred_val": "#0074D9",
                "color_pred_test": "#FF4136",
            },
            "model": {
                "input_size": 1, # since we are only using 1 feature, close price
                "num_lstm_layers": 2,
                "lstm_size": 32,
                "dropout": 0.2,
            },
            "training": {
                "device": "cpu", # "cuda" or "cpu"
                "batch_size": 64,
                "num_epoch": 100,
                "learning_rate": 0.01,
                "scheduler_step_size": 40,
            }
        }

    # functions
    # def download_data(self, config):
    #     ts = TimeSeries(key=config['alpha_vantage']['key']) #you can use the demo API key for this project, but please make sure to eventually get your own API key at https://www.alphavantage.co/support/#api-key. 
    #     data, meta_data = ts.get_daily_adjusted(config["alpha_vantage"]["symbol"], outputsize=config["alpha_vantage"]["outputsize"])

    #     data_date = [date for date in data.keys()]
    #     data_date.reverse()

    #     data_close_price = [float(data[date][config["alpha_vantage"]["key_adjusted_close"]]) for date in data.keys()]
    #     data_close_price.reverse()
    #     data_close_price = np.array(data_close_price)

    #     num_data_points = len(data_date)
    #     display_date_range = "from " + data_date[0] + " to " + data_date[num_data_points-1]
    #     print("Number data points", num_data_points, display_date_range)

    #     return data_date, data_close_price, num_data_points, display_date_range

    def download_data(self):
        ticker = yf.Ticker(self.config['yf']['symbol'])
        data = ticker.history(start="2010-01-01")
        data = data.reset_index()

        data_date = data['Date']
        # data_date.reverse()

        data_close_price = data['Close']
        # data_close_price.reverse()
        data_close_price = np.array(data_close_price)

        num_data_points = data_date.shape[0]
        display_date_range = "from " + str(data_date[0]) + " to " + str(data_date[num_data_points-1])
        print("Number data points", num_data_points, display_date_range)

        return data, data_date, data_close_price, num_data_points, display_date_range