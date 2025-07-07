#!/data/data/com.termux/files/usr/bin/bash

echo "🔄 Pulling latest changes from GitHub..."
cd ~/CryptoFuturesBot || exit

git stash        # Save any local changes
git pull origin master
git stash pop    # Restore local changes (optional)

echo "✅ Update complete!"
