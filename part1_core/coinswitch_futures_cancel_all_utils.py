import requests
import time
import json
import logging
from coinswitch_signature_utils import generate_signature
from dotenv import load_dotenv
import os

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

API_KEY = os.getenv("COINSWITCH_API_KEY")
API_SECRET = os.getenv("COINSWITCH_SECRET_KEY")

# Base URL and endpoint
BASE_URL = "https://coinswitch.co"
endpoint = "/trade/api/v2/futures/cancel_all"
method = "POST"

# Parameters
payload = {
    "exchange": "EXCHANGE_2",   # Mandatory
    # Optional → you can cancel specific symbol only:
    # "symbol": "BTCUSDT"       # uncomment to cancel one symbol
}

# Main function
def cancel_all_orders():
    try:
        epoch_time = str(int(time.time() * 1000))
        params = {}  # No GET params needed

        # Generate signature
        signature = generate_signature(method, endpoint, params, epoch_time)

        url = BASE_URL + endpoint

        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-SIGNATURE': signature,
            'X-AUTH-APIKEY': API_KEY,
            'X-AUTH-EPOCH': epoch_time
        }

        # Send request
        logging.info(f"Sending Cancel ALL Orders request...")
        response = requests.request(method, url, headers=headers, json=payload)

        # Log response
        logging.info(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            logging.info("Successfully cancelled orders!")
            print(json.dumps(response.json(), indent=2))
        else:
            logging.error(f"Failed to cancel orders: {response.status_code} - {response.text}")

    except Exception as e:
        logging.error(f"Exception occurred while cancelling orders: {e}")

# Entry point
if __name__ == "__main__":
    logging.info("Starting Futures Cancel All Orders...")
    cancel_all_orders()
    logging.info("Completed Cancel All Orders.")

