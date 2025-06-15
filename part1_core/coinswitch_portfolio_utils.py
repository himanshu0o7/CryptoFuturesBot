# coinswitch_portfolio_utils.py

import requests
import time
import logging
import json
from coinswitch_signature_utils import generate_signature
from dotenv import load_dotenv
import os

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load env variables
load_dotenv()
API_KEY = os.getenv("COINSWITCH_API_KEY")
API_SECRET = os.getenv("COINSWITCH_SECRET_KEY")

# Endpoint details
endpoint = "/trade/api/v2/user/portfolio"
method = "GET"
payload = {}
params = {}  # No params required

# Prepare signature
epoch_time = str(int(time.time() * 1000))
from coinswitch_env_loader import API_KEY, secret_key

# Full URL
url = "https://coinswitch.co" + endpoint

# Headers
headers = {
    'Content-Type': 'application/json',
    'X-AUTH-SIGNATURE': signature,
    'X-AUTH-APIKEY': API_KEY,
    'X-AUTH-EPOCH': epoch_time
}

# API Call
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

