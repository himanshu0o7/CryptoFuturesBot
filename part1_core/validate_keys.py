# part1_core/validate_keys.py
from coinswitch_api_utils import send_request

print("[INFO] Validating Coinswitch API keys...")

response = send_request("GET", "/trade/api/v2/validate/keys")

if response and response.get("message") == "Valid Access":
    print("[SUCCESS] API Keys are valid!")
else:
    print("[ERROR] API Keys are invalid!")

