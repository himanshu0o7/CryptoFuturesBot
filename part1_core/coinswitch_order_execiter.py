import json
import logging
import time
from datetime import datetime
from coinswitch_futures_order_utils import place_futures_order

# Setup logging
logging.basicConfig(level=logging.INFO)

SIGNALS_FILE = "signal_generator.json"
ORDERS_LOG_FILE = "orders_log.json"

# Load signals
try:
    logging.info("Loading signals from signal_generator.json...")
    with open(SIGNALS_FILE, "r") as f:
        signals = json.load(f)
except (json.JSONDecodeError, FileNotFoundError) as e:
    logging.error(f"Error loading signals: {e}")
    signals = {}

# Prepare orders log
orders_log = []

# Process BUY signals
for buy_signal in signals.get("BUY", []):
    try:
        symbol = buy_signal.get("symbol", "")
        if not symbol:
            continue

        # Place BUY order
        result = place_futures_order(
            symbol=symbol,
            side="BUY",
            order_type="MARKET",  # You can change to "LIMIT" if needed
            qty=10,  # Adjust quantity logic if required
            price=None,
            trigger_price=None,
            reduce_only=False,
        )

        if result:
            log_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "symbol": symbol,
                "side": "BUY",
                "order_id": result["order_id"],
                "status": result["status"],
                "exec_quantity": result["exec_quantity"],
                "avg_execution_price": result["avg_execution_price"],
                "realised_pnl": result["realised_pnl"],
            }
            orders_log.append(log_entry)

        time.sleep(1)  # Small delay to avoid API rate limits

    except Exception as e:
        logging.error(f"Error processing BUY signal {buy_signal}: {e}")

# Process SELL signals
for sell_signal in signals.get("SELL", []):
    try:
        symbol = sell_signal.get("symbol", "")
        if not symbol:
            continue

        # Place SELL order
        result = place_futures_order(
            symbol=symbol,
            side="SELL",
            order_type="MARKET",  # You can change to "LIMIT" if needed
            qty=10,  # Adjust quantity logic if required
            price=None,
            trigger_price=None,
            reduce_only=True,  # SELL usually reduce_only=True in Futures
        )

        if result:
            log_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "symbol": symbol,
                "side": "SELL",
                "order_id": result["order_id"],
                "status": result["status"],
                "exec_quantity": result["exec_quantity"],
                "avg_execution_price": result["avg_execution_price"],
                "realised_pnl": result["realised_pnl"],
            }
            orders_log.append(log_entry)

        time.sleep(1)  # Small delay to avoid API rate limits

    except Exception as e:
        logging.error(f"Error processing SELL signal {sell_signal}: {e}")

# Save orders log
try:
    with open(ORDERS_LOG_FILE, "w") as f:
        json.dump(orders_log, f, indent=4)
    logging.info(f"[SUCCESS] All orders processed. Log saved to {ORDERS_LOG_FILE}")
except Exception as e:
    logging.error(f"Error saving orders log: {e}")
