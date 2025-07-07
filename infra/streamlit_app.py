import json
import time
import pandas as pd

try:
    import streamlit as st
    import plotly.graph_objects as go
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False

try:
    from coinswitch_api_utils import send_request
except ImportError:
    def send_request(method, endpoint):
        print(f"[Mock] {method} request to {endpoint}")
        return {"data": {"available_balance": 100.0}}

try:
    from coinswitch_api import CoinswitchAPI
except ImportError:
    class CoinswitchAPI:
        def __init__(self, symbol):
            self.symbol = symbol
            self.candles = []
        def start_candle_stream(self):
            print("[Mock] Starting candle stream")
        def get_positions(self):
            return []
        def place_order(self, side, quantity):
            print(f"[Mock] Placing {side} order for {quantity}")
        def close_position(self):
            print("[Mock] Closing position")

if STREAMLIT_AVAILABLE:
    st.set_page_config(page_title="CryptoFuturesBot", layout="wide")

    mode = st.sidebar.radio("Mode", ["Paper", "Live"])
    st.session_state["live_mode"] = mode == "Live"
    symbol = st.sidebar.text_input("Symbol", value="BTCUSDT")

    api = st.session_state.get("api")
    if api is None or not isinstance(api, CoinswitchAPI) or api.symbol != symbol:
        api = CoinswitchAPI(symbol)
        api.start_candle_stream()
        st.session_state["api"] = api

    st.title("CryptoFuturesBot Dashboard")

    st.subheader("Account Overview")
    wallet_data = send_request("GET", "/trade/api/v2/futures/wallet_balance")
    balance = wallet_data.get("data", {}).get("available_balance") if wallet_data else None
    if balance is not None:
        st.metric("Wallet Balance", balance)
    else:
        st.warning("Failed to fetch wallet balance")

    st.subheader("Last Five Trades")
    try:
        with open("orders_log.json") as f:
            orders = json.load(f)
        last_trades = orders[-5:] if isinstance(orders, list) else []
        if last_trades:
            st.table(last_trades)
        else:
            st.info("No trades recorded")
    except Exception as exc:
        st.error(f"Error loading orders_log.json: {exc}")

    st.subheader("Signals")
    try:
        with open("signal_generator.json") as f:
            signals = json.load(f)
        st.json(signals)
    except Exception as exc:
        st.error(f"Error loading signal_generator.json: {exc}")

    st.title(f"Candles for {symbol} (5m)")
    st.experimental_set_query_params(refresh=str(time.time()))

    candles = getattr(api, "candles", [])[-60:]
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
    try:
        positions = api.get_positions()
        if positions:
            st.table(positions)
        else:
            st.write("No active positions")
    except Exception as exc:
        st.error(f"Error fetching active positions: {exc}")

    st.subheader("Manual Trading")
    col1, col2, col3 = st.columns(3)
    if col1.button("BUY"):
        try:
            api.place_order("buy", 1)
        except Exception as exc:
            st.error(f"Buy order failed: {exc}")
    if col2.button("SELL"):
        try:
            api.place_order("sell", 1)
        except Exception as exc:
            st.error(f"Sell order failed: {exc}")
    if col3.button("EXIT"):
        try:
            api.close_position()
        except Exception as exc:
            st.error(f"Exit position failed: {exc}")
else:
    print("Streamlit and/or Plotly is not installed. Please install required packages and run this script in a local environment.")
