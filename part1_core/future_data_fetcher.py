# part1_core/future_data_fetcher.py

import json
import time
from coinswitch_api_utils import send_request


def fetch_futures_data():
    print("[INFO] Fetching 24hr ticker data (Coinswitch)...")

    endpoint = "/trade/api/v2/24hr/all-pairs/ticker"
    method = "GET"

    params = {"exchange": "coinswitchx"}  # REQUIRED PARAM!

    response = send_request(method, endpoint, params)

    if response is None:
        print("[ERROR] Failed to fetch ticker data!")
        return

    try:
        data = response["data"]  # correct!
        print(f"[SUCCESS] Ticker data fetched for {len(data)} pairs.")

        with open("futures_data.json", "w") as f:
            json.dump(data, f, indent=4)

        print("[SUCCESS] Futures data saved to futures_data.json")

    except Exception as e:
        print(f"[ERROR] Failed to process ticker data: {e}")


if __name__ == "__main__":
    fetch_futures_data()
