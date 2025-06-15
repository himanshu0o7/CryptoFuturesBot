# part1_core/coinswitch_api_utils.py
import requests
import json
import time
import os
from cryptography.hazmat.primitives.asymmetric import ed25519
from dotenv import load_dotenv
from urllib.parse import urlparse, urlencode
import urllib

load_dotenv()

API_KEY = os.getenv("COINSWITCH_API_KEY")
SECRET_KEY = os.getenv("COINSWITCH_SECRET_KEY")

def get_server_time():
    url = "https://coinswitch.co/trade/api/v2/time"
    response = requests.get(url)
    return str(response.json().get("serverTime", int(time.time() * 1000)))

def get_signature(method, endpoint, params=None, payload=None):
    if params is None:
        params = {}
    if payload is None:
        payload = {}

    unquote_endpoint = endpoint
    if method == "GET" and len(params) != 0:
        endpoint += ('&', '?')[urlparse(endpoint).query == ''] + urlencode(params)
        unquote_endpoint = urllib.parse.unquote_plus(endpoint)

    if method == "GET":
        signature_msg = method + unquote_endpoint + json.dumps(payload, separators=(',', ':'), sort_keys=True)
    else:
        signature_msg = method + unquote_endpoint + json.dumps(payload, separators=(',', ':'), sort_keys=True)

    request_string = bytes(signature_msg, 'utf-8')
    secret_key_bytes = bytes.fromhex(SECRET_KEY)
    secret_key = ed25519.Ed25519PrivateKey.from_private_bytes(secret_key_bytes)
    signature_bytes = secret_key.sign(request_string)
    signature = signature_bytes.hex()

    return signature

def send_request(method, endpoint, params=None, payload=None):
    if params is None:
        params = {}
    if payload is None:
        payload = {}

    signature = get_signature(method, endpoint, params, payload)
    url = "https://coinswitch.co" + endpoint

    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-SIGNATURE': signature,
        'X-AUTH-APIKEY': API_KEY
    }

    if method == "GET":
        response = requests.get(url, headers=headers, params=params)
    elif method == "POST":
        response = requests.post(url, headers=headers, json=payload)
    elif method == "DELETE":
        response = requests.delete(url, headers=headers, json=payload)
    else:
        raise Exception(f"Unsupported method: {method}")

    if response.status_code != 200:
        print(f"[ERROR] API Request failed: {response.status_code} - {response.text}")
        return None

    return response.json()

