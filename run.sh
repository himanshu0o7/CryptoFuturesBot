#!/bin/bash
 codex/generate-requirements.txt-and-add-run.sh
# Simple launcher for CryptoFuturesBot
# Loads environment variables and runs main.py

# Exit on error
set -e

# Load .env if present
if [ -f ".env" ]; then
  # export all variables defined in .env
  set -a
  source .env
  set +a
fi

exec python main.py

# Wrapper script to execute the full bot
bash run_all.sh "$@"
 master
