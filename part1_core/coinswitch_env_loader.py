# part1_core/coinswitch_env_loader.py

import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

API_KEY = os.getenv("COINSWITCH_API_KEY")
secret_key = os.getenv("COINSWITCH_SECRET_KEY")

if not API_KEY or not secret_key:
    raise ValueError(
        "ERROR: API_KEY or SECRET_KEY is missing! Please check your .env file."
    )
