# part1_core/coinswitch_ws_candles.py

import socketio
import json
import time

# CONFIG
base_url = "https://ws.coinswitch.co/"
namespace = "/pro/realtime-rates-socket/futures/exchange_2"

pair = "BTCUSDT_5"  # BTCUSDT_5 → 5-min candles. You can also use BTCUSDT_1, BTCUSDT_15 etc.

sio = socketio.Client()


@sio.event
def connect():
    print("✅ Connected to Coinswitch WS - CANDLES")
    subscribe_data = {"event": "subscribe", "pair": pair}
    sio.emit("FETCH_CANDLESTICK_CS_PRO", subscribe_data, namespace=namespace)


@sio.on("FETCH_CANDLESTICK_CS_PRO", namespace=namespace)
def on_message(data):
    print("========== Live Candle Update ==========")
    print(json.dumps(data, indent=2))


@sio.event
def disconnect():
    print("❌ Disconnected from Candles WS")


sio.connect(
    url=base_url,
    namespaces=[namespace],
    transports="websocket",
    socketio_path="/pro/realtime-rates-socket/futures/exchange_2",
    wait=True,
    wait_timeout=3600,
)

sio.wait()
