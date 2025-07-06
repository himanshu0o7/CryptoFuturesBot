✅ main.py — Entry script for CryptoFuturesBot

import os import ccxt import pandas as pd import pandas_ta as ta from dotenv import load_dotenv import time import logging import telegram from datetime import datetime

--- Load API keys from .env ---

load_dotenv() TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN") TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

--- Initialize Telegram Bot ---

bot = telegram.Bot(token=TELEGRAM_TOKEN)

--- Setup Logging ---

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

--- Initialize Exchange (Example: Binance) ---

exchange = ccxt.binance({ 'enableRateLimit': True })

SYMBOL = 'BTC/USDT' TIMEFRAME = '5m' LIMIT = 100

def fetch_ohlcv(): logging.info(f"Fetching data for {SYMBOL}...") ohlcv = exchange.fetch_ohlcv(SYMBOL, timeframe=TIMEFRAME, limit=LIMIT) df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']) df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms') return df

def apply_strategy(df): df.ta.ema(length=9, append=True) df.ta.ema(length=21, append=True) df['signal'] = 0 df.loc[df['EMA_9'] > df['EMA_21'], 'signal'] = 1 df.loc[df['EMA_9'] < df['EMA_21'], 'signal'] = -1 return df

def send_telegram_message(message): try: bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message) logging.info(f"Telegram alert sent: {message}") except Exception as e: logging.error(f"Failed to send Telegram message: {e}")

def run(): df = fetch_ohlcv() df = apply_strategy(df) latest = df.iloc[-1] signal = latest['signal']

if signal == 1:
    send_telegram_message("🚀 BUY Signal for BTC/USDT (EMA Crossover)")
elif signal == -1:
    send_telegram_message("🔻 SELL Signal for BTC/USDT (EMA Crossover)")
else:
    logging.info("No clear signal.")

if name == "main": while True: try: run() time.sleep(300)  # 5 minutes interval except Exception as e: logging.error(f"Error in main loop: {e}") time.sleep(60)

