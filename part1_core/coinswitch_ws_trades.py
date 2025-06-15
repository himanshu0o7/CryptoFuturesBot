# part1_core/coinswitch_ws_trades.py

import socketio

# Base WebSocket URL and config
base_url = "wss://ws.coinswitch.co/"
namespace = "/exchange_2"
socketio_path = "/pro/realtime-rates-socket/futures/exchange_2"

# Event name for TRADES
FETCH_TRADES_CS_PRO = "FETCH_TRADES_CS_PRO"

# Example pair → make dynamic later
pair = "BTCUSDT"

# Initialize Socket.IO client
sio = socketio.Client()

@sio.on(FETCH_TRADES_CS_PRO, namespace=namespace)
def on_trades(data):
    print("========== Received Trades ==========")
    for trade in data.get("data", []):
        print(f"Time: {trade['E']} | Price: {trade['p']} | Qty: {trade['q']} | Symbol: {trade['s']} | Maker? {trade['m']}")
    print("=====================================")

def main():
    print(f"[INFO] Connecting to WebSocket for pair: {pair}")
    sio.connect(url=base_url, namespaces=[namespace], transports=['websocket'],
                socketio_path=socketio_path, wait=True, wait_timeout=3600)
    
    subscribe_data = {
        'event': 'subscribe',
        'pair': pair
    }

    print(f"[INFO] Subscribing to TRADES...")
    sio.emit(FETCH_TRADES_CS_PRO, subscribe_data, namespace=namespace)

    print(f"[INFO] Listening... Press CTRL+C to exit.")
    sio.wait()

if __name__ == "__main__":
    main()

