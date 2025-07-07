import requests
import json
import logging
import time
from urllib.parse import urlparse, urlencode
from coinswitch_signature_utils import generate_signature
from coinswitch_env_loader import API_KEY, secret_key

# Logging config
logging.basicConfig(level=logging.INFO)

# Order parameters
symbol = "DOGEUSDT"
exchange = "EXCHANGE_2"
price = 0.28
side = "BUY"
order_type = "LIMIT"
quantity = 22
trigger_price = 0.30
reduce_only = False

# API endpoint details
method = "POST"
endpoint = "/trade/api/v2/futures/order"
params = {}  # For POST, usually no query params

# Prepare epoch time
epoch_time = str(int(time.time() * 1000))

# Generate signature
signature = generate_signature(method, endpoint, params, epoch_time, secret_key)

# Full URL
url = "https://coinswitch.co" + endpoint

# Headers
headers = {
    "Content-Type": "application/json",
    "X-AUTH-SIGNATURE": signature,
    "X-AUTH-APIKEY": API_KEY,
    "X-AUTH-EPOCH": epoch_time,
}

# Request body
payload = {
    "symbol": symbol,
    "exchange": exchange,
    "price": price,
    "side": side,
    "order_type": order_type,
    "quantity": quantity,
    "trigger_price": trigger_price,
    "reduce_only": reduce_only,
}

# Send request
logging.info("Starting Place Order...")
try:
    response = requests.post(url, headers=headers, json=payload)
    logging.info(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        logging.info("Order placed successfully!")
        logging.info(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        logging.error(
            f"Failed to place order: {response.status_code} - {response.text}"
        )
except Exception as e:
    logging.error(f"Exception occurred: {e}")
