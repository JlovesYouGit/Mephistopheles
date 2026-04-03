#!/bin/bash

# register_phantasm.sh
# Automates the installation of the Lore-Memory Convergence Protocol as a Mac Launch Agent.

PLIST_NAME="com.phantasm.bioglobe.plist"
PLIST_SRC="/Users/u/Desktop/optimised update-v2macos/protocol/$PLIST_NAME"
PLIST_DEST="$HOME/Library/LaunchAgents/$PLIST_NAME"

echo "⚙️  Installing Phantasm Protocol Background Service..."

# Copy to LaunchAgents
cp "$PLIST_SRC" "$PLIST_DEST"

# Load the daemon
launchctl unload "$PLIST_DEST" 2>/dev/null
launchctl load "$PLIST_DEST"

echo "✅ Phantasm Protocol is now active and resident in the background."
echo "📟 Log: /Users/u/Desktop/optimised update-v2macos/protocol/bioglobe.log"
echo "📟 Error: /Users/u/Desktop/optimised update-v2macos/protocol/bioglobe.err"
