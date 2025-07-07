# CryptoFuturesBot

## Overview
CryptoFuturesBot is an experimental trading bot framework. It provides several
modules for interacting with the CoinSwitch exchange and running strategy code.
The repository includes utilities for signal generation, order execution and a
Telegram notification system.

## Setup
1. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. **Install dependencies**
   ```bash
   pip install cryptography requests python-dotenv pandas ccxt pandas-ta python-telegram-bot
   ```

## Environment variables
Copy `.env.sample` to `.env` and fill in the values:

- `COINSWITCH_API_KEY`
- `COINSWITCH_SECRET_KEY`
- `OPENAI_API_KEY`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

You can validate your environment using `validate_env.sh`.

## Running the bot
Execute the main entry script:
```bash
./run.sh
```
