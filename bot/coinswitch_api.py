import os
from dotenv import load_dotenv
from coinswitch_api_utils import send_request

load_dotenv()

API_KEY = os.getenv("COINSWITCH_API_KEY")
SECRET_KEY = os.getenv("COINSWITCH_SECRET_KEY")


def fetch_candles(symbol: str, interval: str = "5m", limit: int = 100):
    """Fetch historical candles for a symbol."""
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit,
        "exchange": "EXCHANGE_2",
    }
    return send_request("GET", "/trade/api/v2/klines", params=params)


def place_order(symbol: str, side: str, quantity: float, leverage: int = 1,
                order_type: str = "MARKET"):
    """Place an order on CoinSwitch."""
    payload = {
        "symbol": symbol,
        "side": side,
        "quantity": quantity,
        "order_type": order_type,
        "leverage": leverage,
        "exchange": "EXCHANGE_2",
    }
    return send_request("POST", "/trade/api/v2/futures/order", payload=payload)

