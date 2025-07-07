import os
import requests
from dotenv import load_dotenv

load_dotenv()

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
    )
    send_message(text)


def alert_sl_tp(event_type, symbol, qty, price) -> None:
    text = (
        f"<b>{event_type} Triggered</b>\n"
        f"Symbol: {symbol}\n"
        f"Qty: {qty}\n"
        f"Price: {price}"
    )
    send_message(text)


def alert_trailing_update(symbol, new_stop) -> None:
    text = (
        f"<b>Trailing Stop Updated</b>\n"
        f"Symbol: {symbol}\n"
        f"New Stop: {new_stop}"
    )
    send_message(text)


if __name__ == "__main__":
    send_message("Telegram bot initialized")
