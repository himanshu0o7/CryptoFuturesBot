# CryptoFuturesBot

This repository contains an experimental futures trading bot. It also includes several helper utilities and backup scripts.

## Setup

1. **Clone the repository** and move into the project directory.
2. **Create a Python virtual environment** and install dependencies:
   ```bash
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
```bash
python3 main_runner.py
```

## Backup Scripts

- `auto_backup.sh` – creates a zip archive of the project (placeholder implementation).
- `backup_coinswitch.sh` – commits bot files to Git and pushes them to GitHub.

These scripts help keep your trading data backed up regularly.

## OpenAI Utilities (Optional)

- `openai_knowledge_tool.py` and `openai_knowledge_search.py` – helper scripts demonstrating calls to OpenAI APIs.
- `codeium_explain_module.py` – example integration for explaining or fixing annotated code blocks.

Set `OPENAI_API_KEY` in your environment to use these utilities.
