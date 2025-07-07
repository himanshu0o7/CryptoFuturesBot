import os
import json
import time
from datetime import datetime

import requests
from dotenv import load_dotenv

try:
    import schedule
except ImportError:
    schedule = None
    print("[ERROR] Missing 'schedule' module. Please install it with 'pip install schedule'.")

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

TELEGRAM_ENABLED = bool(BOT_TOKEN and CHAT_ID)
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage" if TELEGRAM_ENABLED else None

def send_telegram(text):
    if not TELEGRAM_ENABLED:
        print(f"[SKIPPED] Telegram disabled: {text}")
        return
    try:
        res = requests.post(API_URL, json={
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": "HTML"
        }, timeout=10)
        res.raise_for_status()
        print("[SUCCESS] Telegram message sent")
    except Exception as e:
        print(f"[ERROR] Failed to send message: {e}")

def alert_trade_execution(order_id, symbol, side, qty, price):
    msg = (
        f"<b>Order Executed</b>\n"
        f"ID: {order_id}\n"
        f"Symbol: {symbol}\n"
        f"Side: {side}\n"
        f"Qty: {qty}\n"
        f"Price: {price}"
    )
    send_telegram(msg)

def alert_signals(buy, sell):
    lines = ["<b>🚀 New Trading Signals</b>"]
    if buy:
        lines.append("\n<b>Buy Signals</b>")
        for s in buy:
            lines.append(f"✅ {s['symbol']} | {s['change_percent']}% | Vol ${s['quote_volume']:,} | Price {s['last_price']}")
    if sell:
        lines.append("\n<b>Sell Signals</b>")
        for s in sell:
            lines.append(f"🔻 {s['symbol']} | {s['change_percent']}% | Vol ${s['quote_volume']:,} | Price {s['last_price']}")
    send_telegram("\n".join(lines))

def alert_sl_tp(event, symbol, qty, price):
    msg = (
        f"<b>{event} Triggered</b>\n"
        f"Symbol: {symbol}\n"
        f"Qty: {qty}\n"
        f"Price: {price}"
    )
    send_telegram(msg)

def alert_trailing_stop(symbol, new_stop):
    send_telegram(
        f"<b>Trailing Stop Updated</b>\n"
        f"Symbol: {symbol}\n"
        f"New Stop: {new_stop}"
    )

def alert_error(message):
    send_telegram(f"<b>Error</b>\n{message}")

def daily_trade_summary():
    try:
        with open("orders_log.json") as f:
            trades = json.load(f)
    except Exception:
        trades = []
    send_telegram(
        f"<b>Daily Summary {datetime.now().date()}</b>\n"
        f"Total trades: {len(trades)}"
    )

def schedule_runner():
    if not schedule:
        print("[ERROR] Cannot run scheduler. 'schedule' module missing.")
        return
    schedule.every().day.at("17:00").do(daily_trade_summary)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    send_telegram("Telegram bot initialized")
