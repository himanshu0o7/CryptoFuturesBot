#!/bin/bash
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

exec python3 main.py
