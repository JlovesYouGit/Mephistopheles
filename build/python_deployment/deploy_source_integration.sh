#!/bin/bash

echo "🚀 Python-Based Source Integration Deployment"
echo "============================================="

# Configuration
DEPLOY_DIR="build/python_deployment"
VENV_PATH="$DEPLOY_DIR/venv"
SRC_PATH="$DEPLOY_DIR/src"
MODULES_PATH="$DEPLOY_DIR/modules"

# Create directory structure
mkdir -p "$VENV_PATH" "$SRC_PATH" "$MODULES_PATH"

echo "📁 Deployment directory: $DEPLOY_DIR"

# Detect system architecture
ARCH=$(uname -m)
echo "🖥️  System architecture: $ARCH"

# Setup Python virtual environment
echo "🐍 Setting up Python virtual environment..."
python3 -m venv "$VENV_PATH"

# Activate virtual environment
source "$VENV_PATH/bin/activate"

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install required packages
echo "📦 Installing required packages..."
pip install pathlib json5 pyobjc-framework-Cocoa

# Create requirements file
cat > "$DEPLOY_DIR/requirements.txt" << 'REQUIREMENTS'
pathlib
json5
pyobjc-framework-Cocoa
REQUIREMENTS

# Create deployment configuration
cat > "$DEPLOY_DIR/config.json" << 'CONFIG'
{
    "source_path": "/Users/u/Desktop/optimised update-v2macos/Sources",
    "target_architecture": "auto_detect",
    "deployment_mode": "full_integration",
    "features": [
        "handler_class_limit_management",
        "optimal_threshold_adjustment",
        "motherboard_routing",
        "voltage_lane_softener", 
        "electromagnetic_discharge_control"
    ],
    "compiler_settings": {
        "optimization_level": "O2",
        "architecture_flags": {
            "x86_64": ["-target", "x86_64-apple-macosx14.0"],
            "arm64": ["-target", "arm64-apple-macosx14.0"]
        }
    }
}
CONFIG

# Create main deployment launcher
cat > "$DEPLOY_DIR/deploy.sh" << 'LAUNCHER'
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
LAUNCHER

# Make scripts executable
chmod +x "$DEPLOY_DIR/deploy.sh"
chmod +x "$SRC_PATH/source_deployer.py"

# Create system service definition
cat > "$DEPLOY_DIR/source_integration_service.plist" << 'SERVICE'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.hardware.optimization.python.integration</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/u/Desktop/optimised update-v2macos/build/python_deployment/deploy.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
    <key>WorkingDirectory</key>
    <string>/Users/u/Desktop/optimised update-v2macos/build/python_deployment</string>
    <key>StandardOutPath</key>
    <string>/Users/u/Desktop/optimised update-v2macos/build/python_deployment/logs/deployment.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/u/Desktop/optimised update-v2macos/build/python_deployment/logs/error.log</string>
</dict>
</plist>
SERVICE

# Create logs directory
mkdir -p "$DEPLOY_DIR/logs"

echo ""
echo "✅ Python deployment system created successfully!"
echo ""
echo "🐍 Virtual Environment: $VENV_PATH"
echo "📄 Source Deployer: $SRC_PATH/source_deployer.py"
echo "⚙️  Configuration: $DEPLOY_DIR/config.json"
echo ""
echo "🔧 Usage:"
echo "  Deploy: $DEPLOY_DIR/deploy.sh"
echo "  Service: $DEPLOY_DIR/source_integration_service.plist"
echo ""
echo "🚀 System ready for Python-based source integration!"
