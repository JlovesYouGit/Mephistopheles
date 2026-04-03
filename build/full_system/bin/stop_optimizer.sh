#!/bin/bash

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$BASE_DIR/../hardware_optimizer.pid"

if [[ -f "$PID_FILE" ]]; then
    PIDS=$(cat "$PID_FILE")
    IFS=':' read -ra PID_ARRAY <<< "$PIDS"
    
    echo "Stopping optimization components..."
    for PID in "${PID_ARRAY[@]}"; do
        if kill -0 "$PID" 2>/dev/null; then
            kill "$PID"
            echo "Stopped process $PID"
        fi
    done
    
    rm -f "$PID_FILE"
    echo "All optimization components stopped"
else
    echo "No optimization components are currently running"
fi
