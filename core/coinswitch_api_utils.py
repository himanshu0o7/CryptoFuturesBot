import json
import os
import time
import urllib
from urllib.parse import urlencode, urlparse

import requests
from cryptography.hazmat.primitives.asymmetric import ed25519
from dotenv import load_dotenv

# Load .env from parent directory if in /core
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=dotenv_path)

COINSWITCH_API_KEY = os.getenv("COINSWITCH_API_KEY")
COINSWITCH_SECRET_KEY = os.getenv("COINSWITCH_SECRET_KEY")

if not COINSWITCH_API_KEY or not COINSWITCH_SECRET_KEY:
    print("[ERROR] Missing COINSWITCH_API_KEY or COINSWITCH_SECRET_KEY in .env!")
    COINSWITCH_API_KEY = None
    COINSWITCH_SECRET_KEY = None

def get_signature(method, endpoint, params, payload=None):
    epoch_time = str(int(time.time() * 1000))
    unquote_endpoint = endpoint
    if method.upper() == "GET" and params:
        endpoint += ('&', '?')[urlparse(endpoint).query == ''] + urlencode(params)
        unquote_endpoint = urllib.parse.unquote_plus(endpoint)

    if payload is not None:
        payload_str = json.dumps(payload, separators=(',', ':'), sort_keys=True)
    else:
        payload_str = json.dumps({}, separators=(',', ':'), sort_keys=True)

    signature_msg = method.upper() + unquote_endpoint + payload_str
    request_string = bytes(signature_msg, 'utf-8')

    try:
        secret_key_bytes = bytes.fromhex(COINSWITCH_SECRET_KEY)
        secret_key = ed25519.Ed25519PrivateKey.from_private_bytes(secret_key_bytes)
        signature_bytes = secret_key.sign(request_string)
        signature = signature_bytes.hex()
    except Exception as e:
        print(f"[ERROR] Signature generation failed: {e}")
        return None, None

    return signature, epoch_time

def send_request(method, endpoint, params={}, payload={}):
    if not COINSWITCH_API_KEY or not COINSWITCH_SECRET_KEY:
        print("[ERROR] API keys not loaded. Check .env!")
        return None

    base_url = "https://coinswitch.co"
    url = base_url + endpoint

    signature, epoch_time = get_signature(method, endpoint, params, payload)
    if not signature:
        return None

    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-SIGNATURE': signature,
        'X-AUTH-APIKEY': COINSWITCH_API_KEY
    }

    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=payload)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers, json=payload)
        else:
            print(f"[ERROR] Unsupported method: {method}")
            return None

        if response.status_code == 200:
            try:
                return response.json()
            except Exception:
                print("[ERROR] Failed to parse JSON!")
                return None
        else:
            print(f"[ERROR] API Request failed: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"[ERROR] Exception during API request: {str(e)}")
        return None
