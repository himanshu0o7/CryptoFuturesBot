# coinswitch_futures_position_utils.py

import requests
import json
import time
import logging
from coinswitch_signature_utils import generate_signature
from dotenv import load_dotenv
import os

# Load .env values
load_dotenv()
API_KEY = os.getenv("COINSWITCH_API_KEY")
API_SECRET = os.getenv("COINSWITCH_SECRET_KEY")

logging.basicConfig(level=logging.INFO)

logging.info("Fetching Futures Positions...")

# NEW endpoint (as per latest API)
endpoint = "/trade/api/v2/user/portfolio"
method = "GET"
params = {}  # No params for portfolio

# Get server time
time_response = requests.get("https://coinswitch.co/trade/api/v2/time")
epoch_time = str(time_response.json().get("server_time", int(time.time() * 1000)))

# Generate signature
signature = generate_signature(method, endpoint, params, epoch_time, API_SECRET)

# Prepare URL
url = "https://coinswitch.co" + endpoint

# Headers
headers = {
    'Content-Type': 'application/json',
    'X-AUTH-SIGNATURE': signature,
    'X-AUTH-APIKEY': API_KEY,
    'X-AUTH-EPOCH': epoch_time
}

# Call API
try:
    response = requests.request(method, url, headers=headers, json=params)
    logging.info(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        logging.info("Futures Positions fetched successfully!")
        data = response.json().get("data", [])

        print("\n========== Futures Positions ==========")
        for item in data:
            currency = item.get("currency", "N/A")
            position_margin = item.get("blocked_balance_future", "N/A")
            main_balance_future = item.get("main_balance_future", "N/A")

            print(f"Symbol: {currency} | Position Margin: {position_margin} | Main Balance (Future): {main_balance_future}")

        print("=======================================\n")
    else:
        logging.error(f"Failed to fetch positions: {response.status_code} - {response.text}")

except Exception as e:
    logging.error(f"Exception occurred: {str(e)}")

logging.info("Completed Futures Positions API.")

