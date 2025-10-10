#!/bin/bash
# Watch Cursor hook logs in real-time

LOG_FILE="/home/nshimokochi/Documents/projects/.cursor/hook_debug.log"

echo "📋 Watching hook logs: $LOG_FILE"
echo "================================================"

# Create log file if it doesn't exist
touch "$LOG_FILE"

# Follow the log file
tail -f "$LOG_FILE"
