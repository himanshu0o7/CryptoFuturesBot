import threading
import socketio
from typing import List, Dict, Optional
from coinswitch_api_utils import send_request

class CoinswitchAPI:
    """Simple wrapper for Coinswitch REST/WebSocket endpoints."""

    def __init__(self, symbol: str = "BTCUSDT"):
        self.symbol = symbol
        self._candles: List[Dict] = []
        self._sio = socketio.Client()
        self._namespace = "/pro/realtime-rates-socket/futures/exchange_2"
        self._pair = f"{symbol}_5"  # 5-minute candles
        self._base_ws_url = "https://ws.coinswitch.co/"
        self._thread: Optional[threading.Thread] = None

    @property
    def candles(self) -> List[Dict]:
        return self._candles

    def _run_socket(self) -> None:
        @self._sio.event
        def connect():
            subscribe = {"event": "subscribe", "pair": self._pair}
            self._sio.emit("FETCH_CANDLESTICK_CS_PRO", subscribe, namespace=self._namespace)

        @self._sio.on("FETCH_CANDLESTICK_CS_PRO", namespace=self._namespace)
        def on_candle(data):
            if isinstance(data, dict) and "data" in data:
                self._candles.append(data["data"])

        self._sio.connect(
            url=self._base_ws_url,
            namespaces=[self._namespace],
            transports="websocket",
            socketio_path="/pro/realtime-rates-socket/futures/exchange_2",
            wait=True,
            wait_timeout=3600,
        )
        self._sio.wait()

    def start_candle_stream(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._thread = threading.Thread(target=self._run_socket, daemon=True)
        self._thread.start()

    def get_positions(self):
        resp = send_request("GET", "/trade/api/v2/user/portfolio")
        if resp and "data" in resp:
            return resp["data"]
        return []

    def place_order(self, side: str, quantity: float, price: float = None, order_type: str = "market"):
        payload = {
            "side": side.lower(),
            "symbol": self.symbol,
            "type": order_type,
            "exchange": "coinswitchx",
            "quantity": quantity,
        }
        if order_type == "limit" and price is not None:
            payload["price"] = price
        return send_request("POST", "/trade/api/v2/order", payload=payload)

    def close_position(self):
        positions = self.get_positions()
        for pos in positions:
            symbol = pos.get("currency")
            if symbol and symbol in self.symbol:
                qty = float(pos.get("position_margin", 0))
                if qty != 0:
                    side = "sell" if qty > 0 else "buy"
                    return self.place_order(side, abs(qty))
        return None
