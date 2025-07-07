import json
import os
import time
from datetime import datetime
from typing import Any

from telegram_bot import send_message

LOG_FILE = "errors.log"


def log_error(msg: str) -> None:
    """Append a timestamped message to the log file."""
    timestamp = datetime.utcnow().isoformat()
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} {msg}\n")


def notify(msg: str) -> None:
    """Send a notification via Telegram and log failures."""
    try:
        send_message(f"⚠️ {msg}")
    except Exception as exc:
        log_error(f"Telegram notify error: {exc}")


def handle_api_response(resp: Any) -> bool:
    """Return False and log/notify if API response indicates failure."""
    if resp is None:
        msg = "API request failed"
        log_error(msg)
        notify(msg)
        return False
    if isinstance(resp, dict) and resp.get("status") == "error":
        msg = f"API error: {resp.get('error', 'Unknown error')}"
        log_error(msg)
        notify(msg)
        return False
    return True


def check_balance(balance: float, required: float) -> bool:
    """Check balance and alert if insufficient."""
    if balance < required:
        msg = f"Insufficient balance: {balance} < {required}"
        log_error(msg)
        notify(msg)
        return False
    return True


def safe_json_loads(data: str):
    """Safely load JSON, logging decode errors."""
    try:
        return json.loads(data)
    except json.JSONDecodeError as exc:
        msg = f"JSON decode error: {exc}"
        log_error(msg)
        notify(msg)
        return None


def check_signal_timeout(start_time: float, timeout: float) -> bool:
    """Return True if a signal operation timed out."""
    if time.time() - start_time > timeout:
        msg = "Signal timeout"
        log_error(msg)
        notify(msg)
        return True
    return False
