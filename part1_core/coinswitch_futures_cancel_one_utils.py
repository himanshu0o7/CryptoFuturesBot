import requests
import time
import logging
import json
from urllib.parse import urlparse, urlencode, quote_plus
from coinswitch_signature_utils import generate_signature
from coinswitch_env_loader import API_KEY, secret_key

# Config logging
logging.basicConfig(level=logging.INFO)


def cancel_one_order(order_id):
    logging.info(f"Starting Cancel ONE Order... Order ID: {order_id}")

    endpoint = "/trade/api/v2/futures/order"
    method = "DELETE"
    params = {"order_id": order_id, "exchange": "EXCHANGE_2"}

    # Epoch time (mandatory now)
    epoch_time = str(int(time.time() * 1000))

    # Signature generation
    signature = generate_signature(method, endpoint, params, epoch_time, secret_key)

    # Build URL with params
    endpoint_with_params = (
        endpoint + ("&", "?")[urlparse(endpoint).query == ""] + urlencode(params)
    )
    url = "https://coinswitch.co" + endpoint_with_params

    headers = {
        "Content-Type": "application/json",
        "X-AUTH-SIGNATURE": signature,
        "X-AUTH-APIKEY": API_KEY,
        "X-AUTH-EPOCH": epoch_time,
    }

    logging.info("Sending Cancel ONE Order request...")

    try:
        response = requests.request(method, url, headers=headers, json={})

        logging.info(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            logging.info("Order cancelled successfully!")
            print(json.dumps(response.json(), indent=2))
        else:
            logging.error(
                f"Failed to cancel order: {response.status_code} - {response.text}"
            )

    except Exception as e:
        logging.error(f"Exception occurred: {e}")

    logging.info("Completed Cancel ONE Order.")


# Example usage:
if __name__ == "__main__":
    # 🛑 Replace this with a valid order_id you want to cancel:
    test_order_id = "REPLACE_WITH_YOUR_ORDER_ID"

    cancel_one_order(test_order_id)
