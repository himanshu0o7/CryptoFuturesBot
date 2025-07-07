# part1_core/api_connector.py

import os
import requests
from dotenv import load_dotenv


def run():
    print("[INFO] Running part1_core.api_connector ...")
    try:
        # Load config.env
        config_path = os.path.join(os.getcwd(), "config.env")
        if os.path.exists(config_path):
            load_dotenv(dotenv_path=config_path)
            print(f"[INFO] config.env loaded.")

            api_key = os.getenv("API_KEY")
            api_secret = os.getenv("API_SECRET")

            # Example: Coinswitch Futures API → GET /v1/time
            url = "https://api-trading.coinswitch.co/v1/time"
            headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}

            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                server_time = response.json()
                print(f"[INFO] Server time response: {server_time}")
            else:
                print(
                    f"[ERROR] API connection failed. Status Code: {response.status_code}"
                )
                print(f"[ERROR] Response: {response.text}")

        else:
            print(f"[WARNING] config.env not found!")

    except Exception as e:
        print(f"[ERROR] api_connector failed: {e}")
