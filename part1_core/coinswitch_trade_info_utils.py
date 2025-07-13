# coinswitch_trade_info_utils.py

import requests
import logging
import time
from urllib.parse import urlencode
from coinswitch_signature_utils import generate_signature
from coinswitch_env_loader import API_KEY, secret_key

logging.basicConfig(level=logging.INFO)

# API config
endpoint = "/trade/api/v2/tradeInfo"
method = "GET"

# REQUIRED PARAM
params = {"exchange": "EXCHANGE_2"}  # REQUIRED - this was missing before!

payload = {}

# Epoch time
epoch_time = str(int(time.time() * 1000))

# Generate signature
signature = generate_signature(method, endpoint, params, epoch_time, secret_key)

# Full URL with params
url = "https://coinswitch.co" + endpoint + "?" + urlencode(params)

# Headers
headers = {
    "Content-Type": "application/json",
    "X-AUTH-SIGNATURE": signature,
    "X-AUTH-APIKEY": API_KEY,
    "X-AUTH-EPOCH": epoch_time,
}

# Call API
logging.info("Fetching Trade Info...")

try:
    response = requests.request(method, url, headers=headers, json=payload)
    logging.info(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        logging.info("Trade Info fetched successfully!")
        print(response.json())
    else:
        logging.error(
            f"Failed to fetch Trade Info: {response.status_code} - {response.text}"
        )

except Exception as e:
    logging.error(f"Exception occurred: {e}")
