import logging
import os
import time

import ccxt
import pandas as pd
import pandas_ta as ta
import telegram
from dotenv import load_dotenv


load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError("TELEGRAM_TOKEN and TELEGRAM_CHAT_ID must be set in the environment.")

bot = telegram.Bot(token=TELEGRAM_TOKEN)
exchange = ccxt.binance({"enableRateLimit": True})

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

SYMBOL = "BTC/USDT"
TIMEFRAME = "5m"
LIMIT = 100


def fetch_ohlcv() -> pd.DataFrame:
    logging.info("Fetching data for %s...", SYMBOL)
    ohlcv = exchange.fetch_ohlcv(SYMBOL, timeframe=TIMEFRAME, limit=LIMIT)
    df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df


def apply_strategy(df: pd.DataFrame) -> pd.DataFrame:
    df.ta.ema(length=9, append=True)
    df.ta.ema(length=21, append=True)
    df["signal"] = 0
    df.loc[df["EMA_9"] > df["EMA_21"], "signal"] = 1
    df.loc[df["EMA_9"] < df["EMA_21"], "signal"] = -1
    return df


def send_telegram_message(message: str) -> None:
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        logging.info("Telegram alert sent: %s", message)
    except Exception as exc:  # noqa: BLE001
        logging.error("Failed to send Telegram message: %s", exc)


def run() -> None:
    df = fetch_ohlcv()
    df = apply_strategy(df)
    latest = df.iloc[-1]
    signal = latest["signal"]
    if signal == 1:
        send_telegram_message("BUY Signal for BTC/USDT (EMA Crossover)")
    elif signal == -1:
        send_telegram_message("SELL Signal for BTC/USDT (EMA Crossover)")
    else:
        logging.info("No clear signal.")


def main() -> None:
    while True:
        try:
            run()
            time.sleep(300)
        except Exception as exc:  # noqa: BLE001
            logging.error("Error in main loop: %s", exc)
            time.sleep(60)


if __name__ == "__main__":
    main()
