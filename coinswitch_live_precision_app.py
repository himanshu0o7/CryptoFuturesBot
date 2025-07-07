import requests
import logging
import json
import csv
import os
import time
from datetime import datetime

# --- Configuration ---
USE_MOCK = True  # Toggle this to False for real API call
API_URL = "https://trade-api.coinswitch.co/v2/exchangePrecision"
API_KEY = os.getenv("COINSWITCH_API_KEY", "your_api_key_here")
EXCHANGES = ["coinswitchx", "wazirx"]
HEADERS = {
    "Content-Type": "application/json",
    "X-API-KEY": API_KEY
}
MAX_RETRIES = 3
RETRY_DELAY = 3  # seconds
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# --- Mocked Fallback ---
MOCKED_DATA = {
    "coinswitchx": {
        "BTC": {"pricePrecision": 2, "quantityPrecision": 6},
        "ETH": {"pricePrecision": 2, "quantityPrecision": 5}
    },
    "wazirx": {
        "BTC": {"pricePrecision": 1, "quantityPrecision": 5},
        "ETH": {"pricePrecision": 2, "quantityPrecision": 4}
    }
}

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO)

# --- Send Telegram Alert ---
def send_telegram_alert(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logging.warning("Telegram credentials not set.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
        logging.info("Telegram alert sent.")
    except Exception as e:
        logging.error(f"Failed to send Telegram alert: {e}")

# --- Fetch Precision ---
def fetch_precision(exchange):
    if USE_MOCK:
        logging.info(f"[MOCK] Returning mocked precision data for {exchange}")
        return MOCKED_DATA.get(exchange, {})

    payload = {"exchange": exchange}
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.post(API_URL, headers=HEADERS, json=payload)
            response.raise_for_status()
            data = response.json()
            logging.info(f"Fetched data for {exchange} on attempt {attempt}")
            return data
        except requests.exceptions.RequestException as e:
            logging.warning(f"Attempt {attempt} failed for {exchange}: {e}")
            if attempt == MAX_RETRIES:
                logging.error(f"All retries failed for {exchange}.")
                send_telegram_alert(f"❌ Failed to fetch precision data for {exchange} after {MAX_RETRIES} attempts.")
            time.sleep(RETRY_DELAY)
    return {}

# --- Export Helpers ---
def get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def export_to_json(data, filename_prefix="precision_data"):
    filename = f"{filename_prefix}_{get_timestamp()}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    logging.info(f"Exported data to {filename}")

def export_to_csv(data, filename_prefix="precision_data"):
    filename = f"{filename_prefix}_{get_timestamp()}.csv"
    with open(filename, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Exchange", "Symbol", "Price Precision", "Quantity Precision"])
        for exchange, symbols in data.items():
            for symbol, precisions in symbols.items():
                writer.writerow([exchange, symbol, precisions['pricePrecision'], precisions['quantityPrecision']])
    logging.info(f"Exported data to {filename}")

# --- Main Logic ---
def main():
    all_data = {}

    for exchange in EXCHANGES:
        print(f"Fetching precision data for {exchange}...")
        precision_data = fetch_precision(exchange)
        if precision_data:
            print(json.dumps(precision_data, indent=2))
            all_data[exchange] = precision_data
        else:
            print(f"Warning: No data received for {exchange}\n")

    if all_data:
        export_to_json(all_data)
        export_to_csv(all_data)
        print("✅ Data exported with timestamp filenames.")
    else:
        print("❌ No precision data to export.")

if __name__ == "__main__":
    main()
