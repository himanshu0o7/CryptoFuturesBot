import logging
import requests
import json
import time
from urllib.parse import urlparse, urlencode, unquote_plus
from coinswitch_signature_utils import generate_signature
from coinswitch_env_loader import API_KEY, secret_key

# Logging
logging.basicConfig(level=logging.INFO)

# API parameters
endpoint = "/trade/api/v2/exchangePrecision"
method = "POST"
payload = {
    "exchange": "EXCHANGE_2"
}

# Epoch time
epoch_time = str(int(time.time() * 1000))

# Params (for GET requests, not used in POST but required by signature function)
params = {}

# Generate signature
signature = generate_signature(method, endpoint, params, epoch_time, secret_key)

# Build final URL
url = "https://coinswitch.co" + endpoint

# Headers
headers = {
    'Content-Type': 'application/json',
    'X-AUTH-SIGNATURE': signature,
    'X-AUTH-APIKEY': API_KEY,
    'X-AUTH-EPOCH': epoch_time
}

# Request
logging.info("Fetching Exchange Precision...")
try:
    response = requests.request(method, url, headers=headers, json=payload)
    logging.info(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        logging.info("Exchange Precision fetched successfully!")
        print(json.dumps(response.json(), indent=2))
    else:
        logging.error(f"Failed to fetch precision: {response.status_code} - {response.text}")

except Exception as e:
    logging.error(f"Exception occurred: {e}")

