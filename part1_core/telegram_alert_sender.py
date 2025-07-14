# part1_core/telegram_alert_sender.py
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("[SUCCESS] Telegram alert sent!")
    else:
        print(
            f"[ERROR] Failed to send Telegram alert: {response.status_code} - {response.text}"
        )


def main():
    try:
        with open("signal_generator.json") as f:
            signals = json.load(f)
    except FileNotFoundError:
        print("[ERROR] signal_generator.json not found! Run signal_generator.py first.")
        return

    message = "<b>🚀 Crypto Signals 🚀</b>\n\n"

    if signals["buy"]:
        message += "📈 <b>Buy Signals</b>\n"
        for signal in signals["buy"]:
            message += f"✅ {signal['symbol']} | {signal['change_percent']}% | Vol ${signal['quote_volume']:,.2f} | Price {signal['last_price']}\n"
    else:
        message += "📈 No Buy Signals\n"

    message += "\n"

    if signals["sell"]:
        message += "📉 <b>Sell Signals</b>\n"
        for signal in signals["sell"]:
            message += f"🔻 {signal['symbol']} | {signal['change_percent']}% | Vol ${signal['quote_volume']:,.2f} | Price {signal['last_price']}\n"
    else:
        message += "📉 No Sell Signals\n"

    send_telegram_message(message)


if __name__ == "__main__":
    main()
