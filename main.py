 codex/refactor-main.py-for-validity
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


"""Main script for CryptoFuturesBot."""

import json
import logging
import os
import time
from datetime import datetime

import ccxt
import pandas as pd
import pandas_ta as ta
from dotenv import load_dotenv

from env_utils import check_required_env_vars
from telegram_bot import send_message


ORDERS_LOG_FILE = "orders_log.json"
SYMBOL = "BTC/USDT"
TIMEFRAME = "5m"
LIMIT = 100


def validate_env() -> dict:
    """Validate required environment variables."""
    required = ["TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"]
    env = check_required_env_vars(required)
    env["LIVE_TRADE_MODE"] = os.getenv("LIVE_TRADE_MODE", "False")
    return env


def fetch_ohlcv(exchange: ccxt.Exchange) -> pd.DataFrame:
    """Fetch OHLCV data from the exchange."""
    logging.info("Fetching data for %s...", SYMBOL)
    ohlcv = exchange.fetch_ohlcv(SYMBOL, timeframe=TIMEFRAME, limit=LIMIT)
    df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df


def apply_strategy(df: pd.DataFrame) -> int:
    """Apply EMA crossover strategy and return signal."""
    df.ta.ema(length=9, append=True)
    df.ta.ema(length=21, append=True)
    df["signal"] = 0
    df.loc[df["EMA_9"] > df["EMA_21"], "signal"] = 1
    df.loc[df["EMA_9"] < df["EMA_21"], "signal"] = -1
    return int(df.iloc[-1]["signal"])


def log_trade(entry: dict) -> None:
    """Append a trade entry to the orders log."""
    try:
        if os.path.exists(ORDERS_LOG_FILE):
            with open(ORDERS_LOG_FILE, "r") as fh:
                data = json.load(fh)
        else:
            data = []
        data.append(entry)
        with open(ORDERS_LOG_FILE, "w") as fh:
            json.dump(data, fh, indent=2)
        logging.info("Trade logged to %s", ORDERS_LOG_FILE)
    except Exception as exc:  # pragma: no cover - log failures don't affect flow
        logging.error("Failed to log trade: %s", exc)


def execute_trade(exchange: ccxt.Exchange, signal: int, live: bool) -> None:
    """Execute trade based on signal and log the result."""
    side = "buy" if signal == 1 else "sell"
    message = "🚀 BUY Signal for {s} (EMA Crossover)" if signal == 1 else "🔻 SELL Signal for {s} (EMA Crossover)"
    send_message(message.format(s=SYMBOL))

    if not live:
        logging.info("LIVE_TRADE_MODE disabled. Skipping order execution.")
        return

    try:
        if signal == 1:
            order = exchange.create_market_buy_order(SYMBOL, 0.001)
        else:
            order = exchange.create_market_sell_order(SYMBOL, 0.001)

        trade_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "symbol": SYMBOL,
            "side": side.upper(),
            "order_id": order.get("id"),
            "price": order.get("average"),
            "amount": order.get("amount"),
        }
        log_trade(trade_entry)
    except Exception as exc:
        logging.error("Trade execution failed: %s", exc)


def main() -> None:
    """Main execution loop."""
    load_dotenv()
    env = validate_env()
    live_mode = env["LIVE_TRADE_MODE"].lower() in {"1", "true", "yes"}

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    exchange = ccxt.binance({"enableRateLimit": True})

    while True:
        try:
            df = fetch_ohlcv(exchange)
            signal = apply_strategy(df)

            if signal in {1, -1}:
                execute_trade(exchange, signal, live_mode)
            else:
                logging.info("No clear signal.")

            time.sleep(300)
        except Exception as exc:
            logging.error("An error occurred in the main loop: %s", exc)
            time.sleep(60)  # Wait a bit before retrying to avoid spamming on persistent errors


if __name__ == "__main__":
    main()

 master

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
