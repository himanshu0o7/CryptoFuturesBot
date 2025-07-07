# CryptoFuturesBot

CryptoFuturesBot is a modular trading bot that integrates with the CoinSwitch API and can send Telegram alerts.  The project uses a simple `.env` configuration so you can keep your credentials separate from the code.

## Installation

1. Clone this repository.
2. (Optional) create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install the Python dependencies:
   ```bash
   pip install -e .
   ```

## Environment Variables

Create a `.env` file in the project root or start from the provided `.env.sample`:

```bash
cp .env.sample .env
```

Populate it with the following values:

- `COINSWITCH_API_KEY` – your CoinSwitch API key.
- `COINSWITCH_SECRET_KEY` – your 64-character hex-encoded Ed25519 private key used to sign API requests.
- `OPENAI_API_KEY` – token for OpenAI features used in helper scripts.
- `TELEGRAM_BOT_TOKEN` – token for the Telegram bot that sends alerts.
- `TELEGRAM_CHAT_ID` – chat ID where the bot should post updates.

You can regenerate `.env.sample` from an existing `.env` using `./generate_env_sample.sh`.

## Running the Main Controller

After configuring the environment variables and installing dependencies, run the controller to start the bot modules:

```bash
python3 main_runner.py
```

This script loads the various modules in sequence.  You can also run `main_runner.py` or `./run_all.sh` for testing individual components.

## Quick Start Example

```bash
# 1. Set up environment
cp .env.sample .env
# edit .env with your keys

# 2. Install dependencies
pip install -e .

# 3. Run the bot
python3 master_controller.py
```
