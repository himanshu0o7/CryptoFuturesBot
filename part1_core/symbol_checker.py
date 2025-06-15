# part1_core/symbol_checker.py

import json
import os

def check_symbols():
    symbols_file = os.path.expanduser('~/CryptoFuturesBot/part1_core/symbols.json')

    if not os.path.exists(symbols_file):
        print("[ERROR] symbols.json not found! Run symbol_loader first.")
        return

    with open(symbols_file, 'r') as f:
        symbols = json.load(f)

    print(f"[INFO] Loaded {len(symbols)} symbols.")
    print("[INFO] Sample symbols:", symbols[:10])

if __name__ == "__main__":
    check_symbols()

