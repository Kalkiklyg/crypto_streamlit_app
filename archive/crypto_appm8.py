#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
from binance.client import Client
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Binance API setup
API_KEY = "af7NIzmXkRqsY6uWfBppnzJiUaK9Bv9eT2LOTEyD9gGBCSFCi1C7ZQNMeKXoiCC5"
API_SECRET = "zgEJcVrEateuk5pJnjpoRTbNeU0TitqsVUWCp7RaWTZrvtfE6yPGd9jCoq1cn2aR"
client = Client(API_KEY, API_SECRET)

# Function to fetch live crypto prices
def get_crypto_prices(symbols):
    data = []
    for symbol in symbols:
        ticker = client.get_ticker(symbol=symbol)
        data.append({
            "Symbol": symbol,
            "Price (USDT)": round(float(ticker['lastPrice']), 2),
            "24h Change (%)": round(float(ticker['priceChangePercent']), 2),
            "24h High": round(float(ticker['highPrice']), 2),
            "24h Low": round(float(ticker['lowPrice']), 2),
            "Volume": round(float(ticker['volume']), 3)
        })
    return pd.DataFrame(data)

# Function to fetch historical data
def get_historical_data(symbol, start_date, end_date):
    klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, start_date, end_date)
    df = pd.DataFrame(klines, columns=["Time", "Open", "High", "Low", "Close", "Volume", "CloseTime", "QuoteAssetVolume", "NumberOfTrades", "TBBAV", "TBQAV", "Ignore"])
    df["Time"] = pd.to_datetime(df["Time"], unit='ms')
    df["Open"] = df["Open"].astype(float)
    df["Close"] = df["Close"].astype(float)
    return df[["Time", "Open", "Close"]]

# Streamlit UI setup
st.title("Cryptocurrency Price Tracker")

# Download CSV button
st.subheader("Download Cryptocurrency Data")
crypto_symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT"]
selected_symbols = st.multiselect("Select cryptocurrencies:", crypto_symbols, default=["BTCUSDT"])
crypto_df = get_crypto_prices(selected_symbols)

# Button to download CSV
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(crypto_df)
st.download_button("Download Data as CSV", data=csv, file_name="crypto_prices.csv", mime='text/csv')

# Display the selected crypto data
st.subheader("Live Cryptocurrency Prices")
st.dataframe(crypto_df)

# Date selection for historical data
st.subheader("Historical Data Analysis")
selected_crypto = st.selectbox("Select a cryptocurrency for historical analysis:", crypto_symbols)
start_date = st.date_input("Start Date", datetime.today() - timedelta(days=30))
end_date = st.date_input("End Date", datetime.today())

if st.button("Show Historical Data"):
    hist_data = get_historical_data(selected_crypto, str(start_date), str(end_date))
    st.dataframe(hist_data)
    
    # Plot historical data
    st.subheader("Price Trend")
    fig, ax = plt.subplots()
    ax.plot(hist_data["Time"], hist_data["Close"], label="Close Price", color='blue')
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USDT)")
    ax.legend()
    st.pyplot(fig)


# In[ ]:




