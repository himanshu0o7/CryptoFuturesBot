import time
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from coinswitch_api import CoinswitchAPI

st.set_page_config(page_title="CryptoFuturesBot", layout="wide")

symbol = st.sidebar.text_input("Symbol", value="BTCUSDT")
api = st.session_state.get("api")
if api is None or api.symbol != symbol:
    api = CoinswitchAPI(symbol)
    api.start_candle_stream()
    st.session_state["api"] = api

st.title(f"Candles for {symbol} (5m)")

# Auto refresh every 5 seconds
st.experimental_set_query_params(refresh=str(time.time()))

candles = api.candles[-60:]
if candles:
    df = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    fig = go.Figure(data=[go.Candlestick(
        x=df["timestamp"],
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
    )])
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Waiting for candle data...")

st.subheader("Active Positions")
positions = api.get_positions()
if positions:
    st.table(positions)
else:
    st.write("No active positions")

st.subheader("Manual Trading")
col1, col2, col3 = st.columns(3)
if col1.button("BUY"):
    api.place_order("buy", 1)
if col2.button("SELL"):
    api.place_order("sell", 1)
if col3.button("EXIT"):
    api.close_position()
