# part1_core/coinswitch_open_orders_utils.py

import requests
import time
import logging
import json
from coinswitch_signature_utils import generate_signature
from coinswitch_env_loader import API_KEY, secret_key


def get_open_orders(exchange="EXCHANGE_2", count=20):
    logging.info(f"Fetching open orders... Exchange={exchange}")

    # Define endpoint & params
    endpoint = "/trade/api/v2/futures/orders"
    method = "GET"

    params = {
        "exchange": exchange,
        "open": True,  # <--- IMPORTANT: filter OPEN orders
        "count": count,
    }

    # Generate required headers
    epoch_time = str(int(time.time() * 1000))
    signature = generate_signature(method, endpoint, params, epoch_time, secret_key)

    url = "https://coinswitch.co" + endpoint
    from urllib.parse import urlparse, urlencode

    url += ("&", "?")[urlparse(url).query == ""] + urlencode(params)

    headers = {
        "Content-Type": "application/json",
        "X-AUTH-SIGNATURE": signature,
        "X-AUTH-APIKEY": API_KEY,
        "X-AUTH-EPOCH": epoch_time,
    }

    try:
        response = requests.get(url, headers=headers)
        logging.info(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            logging.info("Open Orders fetched successfully!")
            response_data = response.json()
            print(json.dumps(response_data.get("data", {}), indent=2))
        else:
            logging.error(
                f"Failed to fetch open orders: {response.status_code} - {response.text}"
            )

    except Exception as e:
        logging.error(f"Exception occurred: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    get_open_orders()
