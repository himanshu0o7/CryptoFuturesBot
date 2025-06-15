#!/bin/bash
cd ~/CryptoFuturesBot

echo "[INFO] Adding files to Git..."

git add futures_data.json signal_generator.json
git add part1_core/*.py
git add part1_core/*.json
git add part1_core/*.txt

echo "[INFO] Committing..."
git commit -m "Backup CoinswitchBot $(date '+%Y-%m-%d %H:%M:%S')"

echo "[INFO] Pushing to GitHub..."
git push

echo "[SUCCESS] Backup complete!"

#!/bin/bash
echo "[INFO] Adding files to Git..."
git add part1_core/futures_data.json part1_core/signal_generator.json part1_core/orders_log.json part1_core/*.txt config.env coinswitch_api_utils.py
git commit -m "Auto backup $(date '+%Y-%m-%d %H:%M:%S')"
echo "[INFO] Pushing to GitHub..."
git push
echo "[SUCCESS] Backup complete!"

