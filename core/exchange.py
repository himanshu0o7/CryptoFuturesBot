import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("COINSWITCH_API_KEY")
BASE_URL = "https://api.coinswitch.co/v2/price"

def fetch_price(symbol="BTCUSDT"):
    try:
        response = requests.get(f"{BASE_URL}?symbol={symbol}", timeout=10)
        response.raise_for_status()
        return float(response.json().get('price'))
    except Exception as e:
        raise Exception(f"Price fetch failed: {e}")
