# part1_core/config_loader.py

import os
from dotenv import load_dotenv


def run():
    print("[INFO] Running part1_core.config_loader ...")
    try:
        # Load config.env
        config_path = os.path.join(os.getcwd(), "config.env")
        if os.path.exists(config_path):
            load_dotenv(dotenv_path=config_path)
            print(f"[INFO] config.env loaded from {config_path}")

            # Example read some keys
            api_key = os.getenv("API_KEY")
            api_secret = os.getenv("API_SECRET")
            print(f"[INFO] API_KEY: {api_key}")
            print(f"[INFO] API_SECRET: {api_secret}")

        else:
            print(f"[WARNING] config.env not found at {config_path}")

    except Exception as e:
        print(f"[ERROR] config_loader failed: {e}")
