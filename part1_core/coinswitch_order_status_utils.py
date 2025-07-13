# coinswitch_cancel_all_utils.py

import requests
import logging
import time
import json
from coinswitch_signature_utils import generate_signature
from coinswitch_env_loader import API_KEY, secret_key

# Setup logging
logging.basicConfig(level=logging.INFO)


def cancel_all_orders(symbol=None):
    endpoint = "/trade/api/v2/futures/cancel_all"
    method = "POST"
    params = {}
    payload = {"exchange": "EXCHANGE_2"}
    if symbol:
        payload["symbol"] = symbol  # Optional: cancel only 1 symbol

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
        logging.info(f"Cancelling all orders... Symbol={symbol if symbol else 'ALL'}")
        response = requests.request(method, url, headers=headers, json=payload)
        logging.info(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            logging.info("Cancel All Orders API success!")
            response_json = response.json()
            print(json.dumps(response_json.get("data", {}), indent=2))
        else:
            logging.error(
                f"Failed to cancel orders: {response.status_code} - {response.text}"
            )

    except Exception as e:
        logging.error(f"Exception occurred: {e}")


if __name__ == "__main__":
    # Example test
    cancel_all_orders()  # Cancel ALL orders
    # cancel_all_orders(symbol="DOGEUSDT")  # Cancel only DOGEUSDT orders
