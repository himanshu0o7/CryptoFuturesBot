import os
import re
import time
import requests
import urllib.parse
from urllib.parse import urlencode
from cryptography.hazmat.primitives.asymmetric import ed25519
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load .env file
load_dotenv()

# Load API credentials from .env
API_KEY = os.getenv("COINSWITCH_API_KEY")
API_SECRET = os.getenv("COINSWITCH_API_SECRET")

# Safety checks
if not API_KEY or not API_SECRET:
    raise ValueError("COINSWITCH_API_KEY and COINSWITCH_API_SECRET must be set in .env!")
if not re.match(r'^[0-9a-fA-F]{64}$', API_SECRET):
    raise ValueError("API_SECRET must be a 64-character hexadecimal string!")

# Signature generator
def get_signature(method, endpoint, params, epoch_time, secret_key):
    unquote_endpoint = endpoint
    if method == "GET" and len(params) != 0:
        endpoint += ('&', '?')[urllib.parse.urlparse(endpoint).query == ''] + urlencode(params)
    unquote_endpoint = urllib.parse.unquote_plus(endpoint)
    signature_msg = method + unquote_endpoint + epoch_time
    request_string = bytes(signature_msg, 'utf-8')
    secret_key_bytes = bytes.fromhex(secret_key)
    private_key = ed25519.Ed25519PrivateKey.from_private_bytes(secret_key_bytes)
    signature_bytes = private_key.sign(request_string)
    signature = signature_bytes.hex()
    return signature

# === STEP 1: Sync server time ===
logging.info("Fetching /time ...")
time_resp = requests.get("https://coinswitch.co/trade/api/v2/time")
time_resp.raise_for_status()

time_data = time_resp.json()
logging.info(f"DEBUG TIME RESPONSE: {time_data}")

# Read serverTime key (correct key!)
server_time = time_data.get("serverTime")
if not server_time:
    raise Exception("Could not extract serverTime from /time response!")

epoch_time = str(server_time)
logging.info(f"Using serverTime: {epoch_time}")

# === STEP 2: Call Trade Info API ===
method = "GET"
endpoint = "/trade/api/v2/tradeInfo"
params = {
    "exchange": "EXCHANGE_2"
}

# Generate signature
signature = get_signature(method, endpoint, params, epoch_time, API_SECRET)

# Build URL
url = "https://coinswitch.co" + endpoint

# Headers
headers = {
    'Content-Type': 'application/json',
    'X-AUTH-SIGNATURE': signature,
    'X-AUTH-APIKEY': API_KEY,
    'X-AUTH-EPOCH': epoch_time
}

# Make API call
logging.info("Fetching Trade Info...")
try:
    response = requests.request(method, url, headers=headers, params=params)
    response.raise_for_status()
    logging.info(f"Trade Info API Response: {response.json()}")
except requests.RequestException as e:
    logging.error(f"Trade Info API request failed: {e}")
    if response is not None:
        logging.error(f"Response Status Code: {response.status_code}")
        logging.error(f"Response Body: {response.text}")
    raise
