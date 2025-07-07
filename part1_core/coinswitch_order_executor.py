# coinswitch_order_executor.py

import requests
import logging
import time
import json
from coinswitch_signature_utils import generate_signature
from coinswitch_env_loader import API_KEY, secret_key

# Setup logging
logging.basicConfig(level=logging.INFO)


def place_order(
    symbol, price, side, order_type, quantity, trigger_price=None, reduce_only=False
):
    endpoint = "/trade/api/v2/futures/order"
    method = "POST"
    params = {}
    payload = {
        "symbol": symbol,
        "exchange": "EXCHANGE_2",
        "price": price,
        "side": side,
        "order_type": order_type,
        "quantity": quantity,
        "reduce_only": reduce_only,
    }
    if trigger_price:
        payload["trigger_price"] = trigger_price

    epoch_time = str(int(time.time() * 1000))
    signature = generate_signature(method, endpoint, params, epoch_time, secret_key)
    url = "https://coinswitch.co" + endpoint

    headers = {
        "Content-Type": "application/json",
        "X-AUTH-SIGNATURE": signature,
        "X-AUTH-APIKEY": API_KEY,
        "X-AUTH-EPOCH": epoch_time,
    }

    try:
        logging.info(
            f"Placing {side} order for {symbol} qty={quantity} @ price={price}"
        )
        response = requests.request(method, url, headers=headers, json=payload)
        logging.info(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            logging.info("Order placed successfully!")
            response_json = response.json()
            print(json.dumps(response_json.get("data", {}), indent=2))
        else:
            logging.error(
                f"Failed to place order: {response.status_code} - {response.text}"
            )

    except Exception as e:
        logging.error(f"Exception occurred: {e}")


if __name__ == "__main__":
    # Example order:
    place_order(
        symbol="DOGEUSDT",
        price=0.28,
        side="BUY",
        order_type="LIMIT",
        quantity=50,
        trigger_price=None,
        reduce_only=False,
    )
