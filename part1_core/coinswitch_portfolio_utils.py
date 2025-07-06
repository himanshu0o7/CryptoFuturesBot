# coinswitch_portfolio_utils.py

import requests
import time
import logging
import json
from coinswitch_signature_utils import generate_signature
from coinswitch_env_loader import API_KEY, secret_key

logging.basicConfig(level=logging.INFO)

endpoint = "/trade/api/v2/user/portfolio"
method = "GET"
params = {}
payload = {}

epoch_time = str(int(time.time() * 1000))
signature = generate_signature(method, endpoint, params, epoch_time, secret_key)

url = "https://coinswitch.co" + endpoint

headers = {
    'Content-Type': 'application/json',
    'X-AUTH-SIGNATURE': signature,
    'X-AUTH-APIKEY': API_KEY,
    'X-AUTH-EPOCH': epoch_time
}

logging.info("Sending Portfolio request...")
response = requests.request(method, url, headers=headers, json=payload)
logging.info(f"Status Code: {response.status_code}")

if response.status_code == 200:
    logging.info("Portfolio fetched successfully!")
    try:
        response_json = response.json()
        print(json.dumps(response_json.get("data", {}), indent=2))
    except Exception as e:
        logging.error(f"Exception occurred while parsing response: {e}")
else:
    logging.error(f"Failed to fetch portfolio: {response.status_code} - {response.text}")

logging.info("Completed Portfolio API.")
