# error_detector.py

import os
import traceback
import sys
from pathlib import Path

# Use current working directory since .env and coinswitch_api_utils are already set up
BASE_DIR = Path(os.getcwd())
sys.path.append(str(BASE_DIR))

from coinswitch_api_utils import send_request

print("Running diagnostics on Coinswitch API key setup...")

try:
    resp = send_request("GET", "/trade/api/v2/futures/wallet_balance")
    if resp:
        print("✅ Wallet Balance API reachable:", resp.get("data", {}).get("available_balance", "[No Balance Info]"))
    else:
        print("❌ API returned None — check key, secret, or endpoint path.")
except Exception as e:
    print("[ERROR DETECTOR] Unhandled exception:")
    traceback.print_exc()
