# auto_backup.sh placeholder
#!/bin/bash

# CryptoFuturesBot auto_backup.sh
# Author: Himanshu's Master Bot Architecture

# Setup
echo "======================================"
echo "🚀 Starting AUTO BACKUP..."
echo "Date: $(date)"
echo "======================================"

# Define backup file name
BACKUP_FILE="CryptoFuturesBot_$(date +%Y%m%d_%H%M%S).zip"

# Create zip excluding venv and previous zips
zip -r "$BACKUP_FILE" . -x "venv/*" "*.zip" "__pycache__/*"

# Check if zip was created
if [ $? -eq 0 ]; then
    echo "✅ Backup created: $BACKUP_FILE"
else
    echo "❌ Backup failed!"
    exit 1
fi

# OPTIONAL → GitHub auto push (you can enable later):
# echo "Pushing backup to GitHub..."
# git add "$BACKUP_FILE"
# git commit -m "Auto backup commit - $(date)"
# git push

echo "======================================"
echo "🎉 AUTO BACKUP COMPLETED!"
echo "======================================"


