# part1_core/futures_data_fetcher.py

import requests
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

BINANCE_FUTURES_API_URL = "https://fapi.binance.com/fapi/v1/ticker/24hr"

def fetch_futures_data():
    symbols_file = os.path.expanduser('~/CryptoFuturesBot/part1_core/symbols.json')
    output_file = os.path.expanduser('~/CryptoFuturesBot/part1_core/futures_data.json')

    if not os.path.exists(symbols_file):
        print("[ERROR] symbols.json not found! Run symbol_loader first.")
        return

    with open(symbols_file, 'r') as f:
        symbols = json.load(f)

    print(f"[INFO] Fetching futures data for {len(symbols)} symbols...")

    all_data = []
    for symbol in symbols:
        try:
            params = {'symbol': symbol}
            response = requests.get(BINANCE_FUTURES_API_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Extract required fields
            futures_info = {
                'symbol': symbol,
                'priceChangePercent': float(data.get('priceChangePercent', 0)),
                'lastPrice': float(data.get('lastPrice', 0)),
                'highPrice': float(data.get('highPrice', 0)),
                'lowPrice': float(data.get('lowPrice', 0)),
                'volume': float(data.get('volume', 0)),
                'quoteVolume': float(data.get('quoteVolume', 0)),
            }

            all_data.append(futures_info)
            print(f"[SUCCESS] {symbol} data fetched.")

            # Sleep to avoid rate limits
            time.sleep(0.1)

        except Exception as e:
            print(f"[ERROR] Failed to fetch data for {symbol}: {e}")

    # Save data
    with open(output_file, 'w') as f:
        json.dump(all_data, f, indent=4)

    print(f"[SUCCESS] Futures data saved to futures_data.json ({len(all_data)} symbols).")

if __name__ == "__main__":
    fetch_futures_data()

