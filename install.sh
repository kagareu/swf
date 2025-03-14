#!/bin/bash

# Define variables
SERVICE_NAME="swf.service"
SERVICE_PATH="/etc/systemd/system/$SERVICE_NAME"
PROJECT_DIR="/opt/swf"
PYTHON_BIN="/usr/bin/python3"

# Ensure the script is run as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

# Install required Python packages
echo "Installing required Python packages..."
$PYTHON_BIN -m pip install -r "$PROJECT_DIR/requirements.txt"

# Create systemd service file
echo "Creating systemd service file..."
cat <<EOF > $SERVICE_PATH
[Unit]
Description=Squid Configuration Manager
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=$PROJECT_DIR
ExecStart=$PYTHON_BIN $PROJECT_DIR/app.py
Restart=always
Environment=FLASK_ENV=production
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd, enable and start the service
echo "Reloading systemd, enabling, and starting the service..."
systemctl daemon-reload
systemctl enable $SERVICE_NAME
systemctl start $SERVICE_NAME

echo "Installation complete. The service is running."