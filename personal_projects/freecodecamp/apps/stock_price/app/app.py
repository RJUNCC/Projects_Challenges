import yfinance as yf
import streamlit as st
import pandas as pd

st.write("""
# Simple stock price app

Shwon are the stock closing **price** and **volume** of Google!

""")

tickerSymbol = st.text_input("Enter ticker symbol: ")

# get data on ticker
tickerData = yf.Ticker(tickerSymbol)

# get historical prices for ticker
tickerDf = tickerData.history(period='id', start='2014-1-1', end='2024-1-1')

st.line_chart(tickerDf.Close)
st.line_chart(tickerDf.Volume)
