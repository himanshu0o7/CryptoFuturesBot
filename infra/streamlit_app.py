codex/update-streamlit_app-and-telegram_bot-functionality
import json
import streamlit as st
from coinswitch_api_utils import send_request

st.set_page_config(page_title="CryptoFuturesBot", layout="wide")

mode = st.sidebar.radio("Mode", ["Paper", "Live"])
st.session_state["live_mode"] = mode == "Live"

st.title("Account Overview")

# Wallet balance
wallet_data = send_request("GET", "/trade/api/v2/futures/wallet_balance")
if wallet_data and "data" in wallet_data:
    balance = wallet_data["data"].get("available_balance", "N/A")
    st.metric("Wallet Balance", balance)
else:
    st.write("Failed to fetch wallet balance")

# Last five trades
st.subheader("Last Five Trades")
try:
    with open("orders_log.json") as f:
        orders = json.load(f)
    last_trades = orders[-5:]
    if last_trades:
        st.table(last_trades)
    else:
        st.write("No trades recorded")
except Exception as exc:
    st.write(f"Error loading orders_log.json: {exc}")

# Signal list
st.subheader("Signals")
try:
    with open("signal_generator.json") as f:
        signals = json.load(f)
    st.json(signals)
except Exception as exc:
    st.write(f"Error loading signal_generator.json: {exc}")

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
 master
