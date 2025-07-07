import json
import os
import time
from datetime import datetime
import requests
import schedule
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


def send_message(text: str) -> None:
    if not TOKEN or not CHAT_ID:
        print("[ERROR] Telegram credentials missing")
        return
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    try:
        requests.post(API_URL, json=payload, timeout=10)
    except Exception as exc:
        print(f"[ERROR] Failed to send message: {exc}")


def alert_trade(trade: dict) -> None:
    text = (
        f"<b>Trade Executed</b>\n"
        f"Symbol: {trade.get('symbol')}\n"
        f"Side: {trade.get('side')}\n"
        f"Qty: {trade.get('qty')}\n"
        f"Price: {trade.get('price')}"
    )
    send_message(text)


def alert_error(msg: str) -> None:
    send_message(f"<b>Error</b>\n{msg}")


def daily_summary() -> None:
    try:
        with open("orders_log.json") as f:
            trades = json.load(f)
    except Exception:
        trades = []
    text = (
        f"<b>Daily Summary {datetime.now().date()}</b>\n"
        f"Total trades: {len(trades)}"
    )
    send_message(text)


def run() -> None:
    schedule.every().day.at("17:00").do(daily_summary)
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    run()
