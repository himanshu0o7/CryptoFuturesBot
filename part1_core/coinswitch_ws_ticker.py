# part1_core/coinswitch_ws_ticker.py

import socketio
import json
import time

# CONFIG
base_url = "https://ws.coinswitch.co/"
namespace = "/pro/realtime-rates-socket/futures/exchange_2"

pair = "BTCUSDT"  # Change this to any pair you want live ticker for!

sio = socketio.Client()

@sio.event
def connect():
    print("✅ Connected to Coinswitch WS - TICKER")
    subscribe_data = {
        'event': 'subscribe',
        'pair': pair
    }
    sio.emit("FETCH_TICKER_INFO_CS_PRO", subscribe_data, namespace=namespace)

@sio.on("FETCH_TICKER_INFO_CS_PRO", namespace=namespace)
def on_message(data):
    print("========== Live Ticker Update ==========")
    print(json.dumps(data, indent=2))

@sio.event
def disconnect():
    print("❌ Disconnected from Ticker WS")

sio.connect(
    url=base_url,
    namespaces=[namespace],
    transports='websocket',
    socketio_path='/pro/realtime-rates-socket/futures/exchange_2',
    wait=True,
    wait_timeout=3600
)

sio.wait()

