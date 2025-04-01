#!/usr/bin/env python
# coding: utf-8

# In[15]:


import streamlit as st
import pandas as pd
from binance.client import Client
import time

# Binance API Keys (Replace with your own keys)
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
client = Client(API_KEY, API_SECRET)

# List of Cryptos to Track
all_symbols = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "ADAUSDT", "BNBUSDT", "SOLUSDT", "DOGEUSDT", "DOTUSDT", "MATICUSDT", "LTCUSDT"]

# Streamlit UI
st.set_page_config(page_title="Crypto Market Tracker", layout="wide")
st.title("Real-Time Cryptocurrency Market Tracker")
st.write("Updated prices fetched directly from Binance API")

# Add a download button
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="crypto_data.csv",
    mime="text/csv"
)

# User selects cryptos to track
selected_symbols = st.multiselect("Select Cryptocurrencies", all_symbols, default=all_symbols[:5])

start_date = st.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
end_date = st.date_input("End Date", value=pd.to_datetime("today"))


def get_crypto_prices(symbols):
    """Fetch real-time prices of selected cryptocurrencies."""
    data = []
    for symbol in symbols:
        ticker = client.get_ticker(symbol=symbol)
        data.append({
            "Symbol": symbol,
            "Price (USDT)": float(ticker['lastPrice']),
            "24h Change (%)": float(ticker['priceChangePercent']),
            "24h High": float(ticker['highPrice']),
            "24h Low": float(ticker['lowPrice']),
            "Volume": float(ticker['volume']),
            "Market Cap": float(ticker['lastPrice']) * float(ticker['quoteVolume']),
            "Open Price": float(ticker['openPrice']),
            "High Price": float(ticker['highPrice']),
            "Low Price": float(ticker['lowPrice'])
            

        })
    return pd.DataFrame(data)


# Fetch and display data
crypto_df = get_crypto_prices(selected_symbols)
st.dataframe(crypto_df, height=400, use_container_width=True)

# Historical Data Analysis
def get_historical_data(symbol, interval='1d', limit=30):
    """Fetch historical data for a given cryptocurrency."""
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(klines, columns=["Open Time", "Open", "High", "Low", "Close", "Volume", "Close Time", "Quote Asset Volume", "Number of Trades", "Taker Buy Base Asset Volume", "Taker Buy Quote Asset Volume", "Ignore"])
    df = df[["Open Time", "Open", "High", "Low", "Close", "Volume"]]
    df["Open Time"] = pd.to_datetime(df["Open Time"], unit='ms')
    df.set_index("Open Time", inplace=True)
    return df

st.subheader("Historical Data Analysis")
selected_crypto = st.selectbox("Select Cryptocurrency for Historical Data", selected_symbols)
historical_df = get_historical_data(selected_crypto)
st.line_chart(historical_df[["Close"]])

# Refresh Button
if st.button("Refresh Prices"):
    st.rerun()

# Run this script with: `streamlit run crypto_app.py`

import pandas as pd
import streamlit as st

# Example DataFrame (Replace with your actual data)
df = pd.DataFrame({
    'Date': ['2024-03-30', '2024-03-31', '2024-04-01'],
    'Crypto': ['Bitcoin', 'Ethereum', 'Solana'],
    'Closing Price': [67000, 3400, 180]
})

# Convert DataFrame to CSV
csv = df.to_csv(index=False).encode('utf-8')





# In[ ]:





# In[20]:





# In[21]:





# In[22]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




