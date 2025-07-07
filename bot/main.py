import os
import time
from dotenv import load_dotenv

from .coinswitch_api import fetch_candles, place_order
from .indicators import detect_breakout
from .telegram_bot import send_message

load_dotenv()

SYMBOL = os.getenv("TRADE_SYMBOL", "BTCUSDT")
QUANTITY = float(os.getenv("TRADE_QTY", "1"))
LEVERAGE = 3


def run_cycle():
    candles_resp = fetch_candles(SYMBOL, "5m", limit=50)
    if not candles_resp or "data" not in candles_resp:
        print("[ERROR] Failed to fetch candles")
        return
    candles = candles_resp["data"]
    signal = detect_breakout(candles)
    if signal == "up":
        res = place_order(SYMBOL, "BUY", QUANTITY, LEVERAGE)
        send_message(f"Breakout UP detected for {SYMBOL}. Order: {res}")
    elif signal == "down":
        res = place_order(SYMBOL, "SELL", QUANTITY, LEVERAGE)
        send_message(f"Breakout DOWN detected for {SYMBOL}. Order: {res}")
    else:
        print("No breakout detected")


def main():
    while True:
        run_cycle()
        time.sleep(5 * 60)


if __name__ == "__main__":
    main()
