#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import pandas as pd
from binance.client import Client
from streamlit_autorefresh import st_autorefresh
import datetime

# Binance API client (replace with your own API keys if needed)
API_KEY='af7NIzmXkRqsY6uWfBppnzJiUaK9Bv9eT2LOTEyD9gGBCSFCi1C7ZQNMeKXoiCC5'
SECRET_KEY='zgEJcVrEateuk5pJnjpoRTbNeU0TitqsVUWCp7RaWTZrvtfE6yPGd9jCoq1cn2aR'
client = Client(API_KEY,SECRET_KEY)

# Function to fetch real-time crypto prices
def get_crypto_prices(symbols):
    data = []
    for symbol in symbols:
        ticker = client.get_ticker(symbol=symbol)
        data.append({
            "Symbol": symbol,
            "Price (USDT)": float(ticker['lastPrice']),
            "24h Change (%)": float(ticker['priceChangePercent']),
            "24h High": float(ticker['highPrice']),
            "24h Low": float(ticker['lowPrice']),
            "Volume": round(float(ticker['quoteVolume']), 3)
        })
    return pd.DataFrame(data)

# Function to fetch historical data
def get_historical_data(symbol, start_date, end_date):
    klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, start_date, end_date)
    df = pd.DataFrame(klines, columns=["Time", "Open", "High", "Low", "Close", "Volume", "CloseTime", "QuoteAssetVolume", "NumberOfTrades", "TakerBuyBaseVolume", "TakerBuyQuoteVolume", "Ignore"])
    df["Time"] = pd.to_datetime(df["Time"], unit='ms')
    return df[["Time", "Open", "High", "Low", "Close", "Volume"]]

# Streamlit app title
st.title("Real-Time Cryptocurrency Dashboard")

# Default cryptocurrencies to display
all_symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT", "SOLUSDT", "DOTUSDT", "MATICUSDT", "LTCUSDT"]

# Allow users to select cryptocurrencies, default to all
selected_symbols = st.multiselect("Select Cryptocurrencies", all_symbols, default=all_symbols)

# Fetch and display data
crypto_df = get_crypto_prices(selected_symbols)
st.dataframe(crypto_df)

# Download CSV for real-time prices
csv = crypto_df.to_csv(index=False).encode('utf-8')
st.download_button("Download Real-Time Data", csv, "real_time_crypto.csv", "text/csv")

# Historical data section
st.subheader("Historical Data Analysis")

# Select a cryptocurrency for historical data
selected_crypto = st.selectbox("Select Cryptocurrency for Historical Data", all_symbols)

# Date selection for historical data
start_date = st.date_input("Start Date", datetime.date(2023, 1, 1))
end_date = st.date_input("End Date", datetime.date.today())

# Fetch and display historical data if selected
if selected_crypto:
    historical_df = get_historical_data(selected_crypto, str(start_date), str(end_date))
    st.dataframe(historical_df)
    
    # Download CSV for historical data
    historical_csv = historical_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Historical Data", historical_csv, "historical_data.csv", "text/csv")

# Auto-refresh every 10 seconds
st_autorefresh(interval=10000, key="refresh")


# In[ ]:




