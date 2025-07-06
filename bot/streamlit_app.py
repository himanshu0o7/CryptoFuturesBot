import streamlit as st
from .coinswitch_api import fetch_candles
from .indicators import detect_breakout

st.title("CryptoFuturesBot Dashboard")

symbol = st.text_input("Symbol", "BTCUSDT")

if st.button("Fetch 5m candles"):
    data = fetch_candles(symbol, "5m", limit=20)
    st.write(data)
    if data and "data" in data:
        signal = detect_breakout(data["data"])
        st.write({"breakout": signal})

