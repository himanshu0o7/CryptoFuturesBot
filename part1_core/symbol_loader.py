# part1_core/symbol_loader.py
import json
from coinswitch_api_utils import send_request

def load_and_save_symbols():
    print("[INFO] Fetching symbols from Coinswitch...")
    params = {"exchange": "coinswitchx"}
    response = send_request("GET", "/trade/api/v2/coins", params)

    if response and "data" in response:
        symbols = response["data"]["coinswitchx"]
        print(f"[SUCCESS] {len(symbols)} symbols fetched.")

        with open("symbols.json", "w") as f:
            json.dump(symbols, f, indent=2)
        print("[SUCCESS] Symbols saved to symbols.json")
    else:
        print("[ERROR] Failed to fetch symbols!")

if __name__ == "__main__":
    load_and_save_symbols()

