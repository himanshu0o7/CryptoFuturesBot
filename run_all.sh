#!/bin/bash

# CryptoFuturesBot run_all.sh
# Author: Himanshu's Master Bot Architecture

# Setup header
echo "======================================"
echo "🚀 Starting CryptoFuturesBot FULL RUN..."
echo "Date: $(date)"
echo "======================================"

# Parts to run
parts=("part1_core" "part2_strategy" "part3_execution" "part4_monitoring" "part5_advanced" "template_modules")

# Run each part using test_runner.py
for part in "${parts[@]}"; do
    echo ""
    echo "======================================"
    echo "▶️ Running $part ..."
    echo "======================================"

    python3 test_runner.py "$part"

    if [ $? -ne 0 ]; then
        echo "❌ Error running $part! Skipping to next..."
    else
        echo "✅ Completed $part."
    fi

    echo ""
done

echo "======================================"
echo "▶️ Running part1_core/api_connector.py ..."
echo "======================================"
python3 -c "import part1_core.api_connector; part1_core.api_connector.run()"
# Final footer
echo "======================================"
echo "🎉 CryptoFuturesBot FULL RUN COMPLETED!"
echo "Date: $(date)"
echo "======================================"


echo "[INFO] Executing Coinswitch Order Executor..."
python3 part1_core/coinswitch_order_executor.py

echo "[INFO] Sending Telegram alert again with final order status..."
python3 part1_core/telegram_alert_sender.py

