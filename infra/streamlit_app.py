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
