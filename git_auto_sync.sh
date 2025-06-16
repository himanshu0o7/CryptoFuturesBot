#!/bin/bash

# Configuration
LOG_FILE="git_sync.log"
BRANCH="master"

# Log the start of the sync process
echo "==========================================" | tee -a "$LOG_FILE"
echo "🕒 Git Sync Started at $(date)" | tee -a "$LOG_FILE"
echo "==========================================" | tee -a "$LOG_FILE"

# Check if the remote 'origin' exists
if ! git remote | grep -q origin; then
    echo "❌ Error: Remote 'origin' does not exist." | tee -a "$LOG_FILE"
    exit 1
fi

# Stage all modified, deleted, or added files
if ! git add . >> "$LOG_FILE" 2>&1; then
    echo "❌ Error: Failed to stage changes." | tee -a "$LOG_FILE"
    exit 1
fi

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo "ℹ️ No changes to commit." | tee -a "$LOG_FILE"
else
    # Commit with timestamp
    COMMIT_MESSAGE="🔄 Auto-sync commit at $(date '+%Y-%m-%d %H:%M:%S')"
    if ! git commit -m "$COMMIT_MESSAGE" >> "$LOG_FILE" 2>&1; then
        echo "❌ Error: Failed to commit changes." | tee -a "$LOG_FILE"
        exit 1
    fi
fi

# Pull with rebase to avoid merge conflicts
if ! git pull --rebase origin "$BRANCH" >> "$LOG_FILE" 2>&1; then
    echo "❌ Error: Failed to pull with rebase. Resolve conflicts and retry." | tee -a "$LOG_FILE"
    exit 1
fi

# Push to the remote repository
if ! git push origin "$BRANCH" >> "$LOG_FILE" 2>&1; then
    echo "❌ Error: Failed to push changes." | tee -a "$LOG_FILE"
    exit 1
fi

# Log the completion of the sync process
echo "✅ Git Sync Completed at $(date)" | tee -a "$LOG_FILE"
echo "==========================================" | tee -a "$LOG_FILE"

