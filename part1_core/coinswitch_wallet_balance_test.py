import requests
import json
import time
import hmac
import hashlib
import os
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load API keys
load_dotenv()
API_KEY = os.getenv("COINSWITCH_API_KEY")
API_SECRET = os.getenv("COINSWITCH_SECRET_KEY")

if not API_KEY or not API_SECRET:
    logging.error("API_KEY or API_SECRET not found in .env! Exiting.")
    exit(1)

# API details
method = "GET"
endpoint = "/trade/api/v2/futures/wallet_balance"
url = "https://coinswitch.co" + endpoint

# Generate timestamp (current unix time in ms)
timestamp = str(int(time.time() * 1000))

# Generate signature
message = f"{method} {endpoint} {timestamp}"
signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()

# Build headers
headers = {
    'Content-Type': 'application/json',
    'X-AUTH-SIGNATURE': signature,
    'X-AUTH-APIKEY': API_KEY,
    'X-AUTH-TIMESTAMP': timestamp
}

# Make request
try:
    logging.info("Sending Wallet Balance request...")
    response = requests.request("GET", url, headers=headers)
    logging.info(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        logging.info("Wallet Balance fetched successfully!")
        print(json.dumps(response.json(), indent=4))
    else:
        logging.error(f"Failed to fetch wallet balance: {response.status_code} - {response.text}")

except Exception as e:
    logging.error(f"An error occurred: {e}")

