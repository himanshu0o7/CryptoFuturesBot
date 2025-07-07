# part1_core/coinswitch_futures_order_utils.py

import requests
import json
import hmac
import hashlib
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load API key and secret from env or config
API_KEY = os.getenv("COINSWITCH_API_KEY", "<your-api-key>")
API_SECRET = os.getenv("COINSWITCH_API_SECRET", "<your-api-secret>")

BASE_URL = "https://coinswitch.co"
ORDER_ENDPOINT = "/trade/api/v2/futures/order"


# Signature generator function
def generate_signature(payload_str, secret_key):
    return hmac.new(
        secret_key.encode(), payload_str.encode(), hashlib.sha256
    ).hexdigest()


# Place order function
def place_futures_order(
    symbol, side, order_type, qty, price=None, trigger_price=None, reduce_only=False
):
    url = BASE_URL + ORDER_ENDPOINT

    payload = {
        "symbol": symbol.lower(),
        "exchange": "EXCHANGE_2",
        "side": side.upper(),
        "order_type": order_type.upper(),
        "quantity": qty,
        "reduce_only": reduce_only,
    }

    # Optional fields
    if order_type.upper() == "LIMIT" and price is not None:
        payload["price"] = price
    if trigger_price is not None:
        payload["trigger_price"] = trigger_price

    # Prepare signature
    payload_str = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
    signature = generate_signature(payload_str, API_SECRET)

    headers = {
        "Content-Type": "application/json",
        "X-AUTH-SIGNATURE": signature,
        "X-AUTH-APIKEY": API_KEY,
    }

    try:
        logging.info(f"Placing {side} {order_type} order for {symbol} qty={qty}...")
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        data = response.json().get("data", {})

        logging.info(
            f"Order placed! Order ID: {data.get('order_id')}, Status: {data.get('status')}"
        )

        return {
            "order_id": data.get("order_id"),
            "status": data.get("status"),
            "exec_quantity": data.get("exec_quantity"),
            "avg_execution_price": data.get("avg_execution_price"),
            "realised_pnl": data.get("realised_pnl"),
        }

    except Exception as e:
        logging.error(f"Error while placing order: {e}")
        return None
