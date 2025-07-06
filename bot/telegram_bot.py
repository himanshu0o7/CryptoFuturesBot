import os
from dotenv import load_dotenv
import requests

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_message(text: str) -> None:
    if not TOKEN or not CHAT_ID:
        print("[ERROR] Telegram credentials missing")
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        r = requests.post(url, json=payload, timeout=10)
        if r.status_code != 200:
            print(f"[ERROR] Telegram error {r.status_code}: {r.text}")
    except Exception as e:
        print(f"[ERROR] Telegram exception: {e}")

