#!/bin/bash

# Activate virtual environment if applicable
# source /path/to/venv/bin/activate

# Export API credentials
export COINSWITCH_API_KEY="your_key_here"
export TELEGRAM_BOT_TOKEN="your_telegram_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"

# Navigate to working directory
cd /path/to/your/project

# Run the script
python3 coinswitch_live_precision_robust.py

# Optional: log output
# python3 coinswitch_live_precision_robust.py >> cron_precision.log 2>&1
