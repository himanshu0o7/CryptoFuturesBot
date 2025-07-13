import logging
import subprocess
import time

logging.basicConfig(level=logging.INFO)

# List of scripts to run in sequence
scripts = [
    "part1_core/coinswitch_wallet_balance_utils.py",
    "part1_core/coinswitch_portfolio_utils.py",
    "part1_core/coinswitch_futures_position_utils.py",
    "part1_core/signal_generator.py",
    "part1_core/coinswitch_order_executor.py",
    "part1_core/coinswitch_pnl_tracker.py",  # safe dummy — prevents crash
]

# Main loop
while True:
    logging.info("===== Starting new trading loop =====")

    for script in scripts:
        logging.info(f"Running {script} ...")
        try:
            result = subprocess.run(["python3", script], check=True, text=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error running {script}: {e}")

    logging.info("===== Sleeping 60 seconds... =====")
    time.sleep(60)
