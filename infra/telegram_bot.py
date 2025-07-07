 codex/update-streamlit_app-and-telegram_bot-functionality
import json
import os
import time
from datetime import datetime
import requests
import schedule

import os
import requests
master
from dotenv import load_dotenv

load_dotenv()

 codex/update-streamlit_app-and-telegram_bot-functionality
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

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError("TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set in the .env file")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


def send_message(text: str) -> None:
    """Send a plain text Telegram message."""
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        resp = requests.post(TELEGRAM_API_URL, json=payload, timeout=10)
        resp.raise_for_status()
    except Exception as exc:
        print(f"[ERROR] Failed to send Telegram message: {exc}")
    else:
        print("[SUCCESS] Telegram message sent")


def alert_new_signals(buy_signals, sell_signals) -> None:
    """Send an alert with lists of buy and sell signals."""
    lines = ["<b>🚀 New Trading Signals</b>"]
    if buy_signals:
        lines.append("\n<b>Buy Signals</b>")
        for s in buy_signals:
            lines.append(f"✅ {s['symbol']} | {s['change_percent']}% | Vol ${s['quote_volume']:,} | Price {s['last_price']}")
    if sell_signals:
        lines.append("\n<b>Sell Signals</b>")
        for s in sell_signals:
            lines.append(f"🔻 {s['symbol']} | {s['change_percent']}% | Vol ${s['quote_volume']:,} | Price {s['last_price']}")
    send_message("\n".join(lines))


def alert_order_executed(order_id, symbol, side, qty, price) -> None:
    text = (
        f"<b>Order Executed</b>\n"
        f"ID: {order_id}\n"
        f"Symbol: {symbol}\n"
        f"Side: {side}\n"
        f"Qty: {qty}\n"
        f"Price: {price}"
 master
    )
    send_message(text)


 codex/update-streamlit_app-and-telegram_bot-functionality
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

def alert_sl_tp(event_type, symbol, qty, price) -> None:
    text = (
        f"<b>{event_type} Triggered</b>\n"
        f"Symbol: {symbol}\n"
        f"Qty: {qty}\n"
        f"Price: {price}"
master
    )
    send_message(text)


 codex/update-streamlit_app-and-telegram_bot-functionality
def run() -> None:
    schedule.every().day.at("17:00").do(daily_summary)
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    run()

def alert_trailing_update(symbol, new_stop) -> None:
    text = (
        f"<b>Trailing Stop Updated</b>\n"
        f"Symbol: {symbol}\n"
        f"New Stop: {new_stop}"
    )
    send_message(text)


if __name__ == "__main__":
    send_message("Telegram bot initialized")
 master
