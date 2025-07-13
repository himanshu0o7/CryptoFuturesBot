from dotenv import load_dotenv
import os

try:
    load_dotenv()
    secret_key = os.getenv("COINSWITCH_SECRET_KEY")
    if not secret_key:
        raise ValueError("COINSWITCH_SECRET_KEY is not set in .env or environment")
    print(f"Secret Key: {secret_key}")
    print(f"Length: {len(secret_key)}")
except Exception as e:
    print(f"Error: {e}")
