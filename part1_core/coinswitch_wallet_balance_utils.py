# coinswitch_wallet_balance_utils.py

import requests
import logging
import time
import json
from coinswitch_signature_utils import generate_signature
from dotenv import load_dotenv
import os

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load API keys from .env
load_dotenv()
from coinswitch_env_loader import API_KEY, secret_key

def get_wallet_balance():
    endpoint = "/trade/api/v2/futures/wallet_balance"
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

    try:
        logging.info("Sending Wallet Balance request...")
        response = requests.request(method, url, headers=headers, json=payload)
        logging.info(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            logging.info("Wallet Balance fetched successfully!")
            response_json = response.json()
            print(json.dumps(response_json.get("data", {}), indent=2))
        else:
            logging.error(f"Failed to fetch wallet balance: {response.status_code} - {response.text}")

    except Exception as e:
        logging.error(f"Exception occurred: {e}")

if __name__ == "__main__":
    get_wallet_balance()

