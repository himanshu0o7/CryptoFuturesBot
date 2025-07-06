# part1_core/coinswitch_futures_pnl_tracker.py

import requests
import json
import logging
import time
from coinswitch_signature_utils import generate_signature
from coinswitch_env_loader import API_KEY, secret_key

endpoint = "/trade/api/v2/futures/wallet_balance"
method = "GET"
params = {}
payload = {}

# Generate epoch time
epoch_time = str(int(time.time() * 1000))

# Generate signature
signature = generate_signature(method, endpoint, params, epoch_time, secret_key)

url = "https://coinswitch.co" + endpoint

headers = {
    'Content-Type': 'application/json',
    'X-AUTH-SIGNATURE': signature,
    'X-AUTH-APIKEY': API_KEY,
    'X-AUTH-EPOCH': epoch_time
}

logging.basicConfig(level=logging.INFO)

logging.info("Fetching Futures Wallet Balance for PnL Tracking...")

response = requests.request(method, url, headers=headers, json=payload)

if response.status_code == 200:
    data = response.json().get("data", {})
    assets = data.get("asset", [])

    # Load LTP from futures_data.json
    try:
        with open("futures_data.json", "r") as f:
            ticker_data = json.load(f)
    except Exception as e:
        logging.error(f"Failed to load futures_data.json: {e}")
        ticker_data = []

    print("\n========== Futures PnL Tracker ==========")
    print(f"{'Symbol':<12} {'Position Margin':>16} {'Blocked Balance':>16} {'Current Price':>16}")

    for asset in assets:
        symbol = asset.get("symbol", "")
        position_margin = float(asset.get("position_margin", "0"))
        blocked_balance = float(asset.get("blocked_balance", "0"))

        # Only show symbols where position_margin > 0
        if position_margin > 0:
            # Find current price from futures_data.json
            current_price = "-"
            for ticker in ticker_data:
                if isinstance(ticker, dict) and ticker.get("symbol", "") == symbol:
                    current_price = ticker.get("lastPrice", "-")
                    break

            print(f"{symbol:<12} {position_margin:>16.4f} {blocked_balance:>16.4f} {current_price:>16}")

    print("=========================================")

else:
    logging.error(f"Failed to fetch wallet balance: {response.status_code} - {response.text}")

