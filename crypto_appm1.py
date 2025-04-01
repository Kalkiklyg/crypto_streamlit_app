#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import pandas as pd
from binance.client import Client
import time
from streamlit_autorefresh import st_autorefresh

# Binance API Keys (Replace with your own keys)
API_KEY = "af7NIzmXkRqsY6uWfBppnzJiUaK9Bv9eT2LOTEyD9gGBCSFCi1C7ZQNMeKXoiCC5"
API_SECRET = "zgEJcVrEateuk5pJnjpoRTbNeU0TitqsVUWCp7RaWTZrvtfE6yPGd9jCoq1cn2aR"
client = Client(API_KEY, API_SECRET)

# List of Cryptos to Track
symbols = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "ADAUSDT", "BNBUSDT", "SOLUSDT", "DOGEUSDT", "DOTUSDT", "MATICUSDT", "LTCUSDT"]

def get_crypto_prices():
    """Fetch real-time prices of selected cryptocurrencies."""
    data = []
    for symbol in symbols:
        ticker = client.get_ticker(symbol=symbol)
        data.append({
            "Symbol": symbol,
            "Price (USDT)": float(ticker['lastPrice']),
            "24h Change (%)": float(ticker['priceChangePercent']),
            "24h Volume": float(ticker['quoteVolume']),
            "Market Cap": float(ticker['lastPrice']) * float(ticker['quoteVolume']),
            "Open Price": float(ticker['openPrice']),
            "High Price": float(ticker['highPrice']),
            "Low Price": float(ticker['lowPrice']),
            "Bid Price": float(ticker['bidPrice']),
            "Ask Price": float(ticker['askPrice'])
        })
    return pd.DataFrame(data)

# Streamlit UI
st.set_page_config(page_title="Crypto Market Tracker", layout="wide")
st.title("Real-Time Cryptocurrency Market Tracker")

st.write("Updated prices fetched directly from Binance API")

# Auto Refresh Every 10 Seconds
st_autorefresh(interval=10000, key="refresh")

# Display Data
crypto_df = get_crypto_prices()
st.dataframe(crypto_df, height=400, use_container_width=True)

# Refresh Button
if st.button("Refresh Prices"):
    st.experimental_rerun()


# In[19]:





# In[20]:





# In[21]:





# In[22]:





# In[23]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




