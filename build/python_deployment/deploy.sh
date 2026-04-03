#!/bin/bash

# Deployment launcher script
DEPLOY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$DEPLOY_DIR/venv"
SRC_PATH="$DEPLOY_DIR/src"

# Activate virtual environment
source "$VENV_PATH/bin/activate"

# Run deployment
echo "🚀 Starting source code deployment..."
python3 "$SRC_PATH/source_deployer.py"

# Deactivate virtual environment
deactivate

echo "🏁 Deployment script completed"
