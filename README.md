# CryptoFuturesBot

 codex/update-readme-and-add-installation-steps
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


codex/rewrite-readme.txt-as-readme.md
## Overview
CryptoFuturesBot is an experimental trading bot framework. It provides several
modules for interacting with the CoinSwitch exchange and running strategy code.
The repository includes utilities for signal generation, order execution and a
Telegram notification system.

## Setup
1. **Create a virtual environment**
   bash
   python3 -m venv venv
   source venv/bin/activate
   
2. **Install dependencies**
   bash
   pip install cryptography requests python-dotenv pandas ccxt pandas-ta python-telegram-bot
   

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


This repository contains an experimental futures trading bot. It also includes several helper utilities and backup scripts.

## Setup

1. **Clone the repository** and move into the project directory.
2. **Create a Python virtual environment** and install dependencies:
   bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt  # create this file with your preferred packages
   ```
3. **Configure environment variables.** Copy `.env.sample` to `.env` and set the following values:
   - `COINSWITCH_API_KEY`
   - `COINSWITCH_SECRET_KEY`
   - `OPENAI_API_KEY` (optional, for OpenAI helper scripts)
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`

Use `generate_env_sample.sh` if you need to generate a template from an existing `.env` file.

## Running the Bot

The trading logic can be launched with one of the main entry points:

- `main.py` – command‑line runner for the bot.
  ```bash
  python3 main.py
  ```
- `streamlit_app.py` – optional Streamlit dashboard if available.
  ```bash
  streamlit run streamlit_app.py
  ```

If you simply want to execute the default loop included in the repository, run `main_runner.py` instead:
 master
```bash
python3 main_runner.py
```

codex/update-readme-and-add-installation-steps
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
## Backup Scripts

- `auto_backup.sh` – creates a zip archive of the project (placeholder implementation).
- `backup_coinswitch.sh` – commits bot files to Git and pushes them to GitHub.

These scripts help keep your trading data backed up regularly.

## OpenAI Utilities (Optional)

- `openai_knowledge_tool.py` and `openai_knowledge_search.py` – helper scripts demonstrating calls to OpenAI APIs.
- `codeium_explain_module.py` – example integration for explaining or fixing annotated code blocks.

Set `OPENAI_API_KEY` in your environment to use these utilities.
 master
 master
