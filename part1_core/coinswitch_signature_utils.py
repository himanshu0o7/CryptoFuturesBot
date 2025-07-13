# coinswitch_signature_utils.py

from cryptography.hazmat.primitives.asymmetric import ed25519
from urllib.parse import urlparse, urlencode
import urllib
import time


def generate_signature(method, endpoint, params, epoch_time, secret_key):
    """
    Generates the X-AUTH-SIGNATURE for CoinSwitch APIs.

    Args:
        method (str): HTTP method (GET, POST, DELETE)
        endpoint (str): API endpoint path
        params (dict): URL query params
        epoch_time (str): Epoch timestamp in milliseconds as string
        secret_key (str): COINSWITCH_SECRET_KEY (hex string)

    Returns:
        str: Signature hex string
    """
    unquote_endpoint = endpoint

    if method == "GET" and len(params) != 0:
        endpoint += ("&", "?")[urlparse(endpoint).query == ""] + urlencode(params)
        unquote_endpoint = urllib.parse.unquote_plus(endpoint)

    # Build signature message
    signature_msg = method + unquote_endpoint + epoch_time

    # Prepare private key
    request_string = bytes(signature_msg, "utf-8")
    secret_key_bytes = bytes.fromhex(secret_key)
    secret_key_obj = ed25519.Ed25519PrivateKey.from_private_bytes(secret_key_bytes)

    # Generate signature
    signature_bytes = secret_key_obj.sign(request_string)
    signature = signature_bytes.hex()

    return signature
