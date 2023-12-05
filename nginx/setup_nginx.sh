#!/bin/bash
# Nginx Setup Script for vproapp

# Update package lists
apt update || { echo "Failed to update package lists"; exit 1; }

# Install Nginx
apt install nginx -y || { echo "Failed to install Nginx"; exit 1; }

# Define upstream application server
APP_SERVER="app:8080"

# Create Nginx configuration for vproapp
CONFIG_FILE="/etc/nginx/sites-available/vproapp"
cat > "$CONFIG_FILE" <<EOT
upstream vproapp {
  server $APP_SERVER;
}

server {
  listen 80;

  location / {
    proxy_pass http://vproapp;
  }
}
EOT

# Symlink configuration and remove default
ln -s "$CONFIG_FILE" /etc/nginx/sites-enabled/vproapp
rm -f /etc/nginx/sites-enabled/default

# Reload Nginx to apply changes
systemctl reload nginx || { echo "Failed to reload Nginx"; exit 1; }

# Enable Nginx to start on boot
systemctl enable nginx

# Leadm signature
echo "Nginx setup complete - Configured by Leadm"
