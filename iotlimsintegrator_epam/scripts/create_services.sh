#!/bin/bash

# Prompt for user input
# shellcheck disable=SC2162
read -p "Enter the username to be added to the www-data group: " USERNAME
# shellcheck disable=SC2162
read -p "Enter the project directory (e.g., /home/ubuntu/blogprojectdrf): " PROJECT_DIR
# shellcheck disable=SC2162
read -p "Enter the Gunicorn socket file path (e.g., /run/gunicorn.sock): " GUNICORN_SOCK
# shellcheck disable=SC2162
read -p "Enter the Gunicorn WSGI application module (e.g., blog.wsgi:application): " GUNICORN_APP

# Function to create and configure gunicorn.socket
setup_gunicorn_socket() {
  cat <<EOL | sudo tee /etc/systemd/system/gunicorn.socket
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=$GUNICORN_SOCK

[Install]
WantedBy=sockets.target
EOL
}

# Function to create and configure gunicorn.service
setup_gunicorn_service() {
  cat <<EOL | sudo tee /etc/systemd/system/gunicorn.service
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=$USERNAME
Group=www-data
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/env/bin/gunicorn \\
          --access-logfile - \\
          --workers 3 \\
          --bind unix:$GUNICORN_SOCK \\
          $GUNICORN_APP

[Install]
WantedBy=multi-user.target
EOL
}

# Function to setup nginx site configuration
setup_nginx() {
  # Print a warning and ask for confirmation
  echo "Warning: This will delete all files in /etc/nginx/sites-enabled/"
  read -p "Are you sure you want to continue? (yes/no): " confirm

  if [ "$confirm" == "yes" ]; then
    # Remove all files in /etc/nginx/sites-enabled/
    sudo rm -r /etc/nginx/sites-enabled/*
    echo "All files in /etc/nginx/sites-enabled/ have been removed."

    # Create the Nginx configuration file for the blog
    sudo tee /etc/nginx/sites-available/blog <<EOL
server {
    listen 80 default_server;
    server_name _;
    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root $PROJECT_DIR;
    }
    location / {
        include proxy_params;
        proxy_pass http://unix:$GUNICORN_SOCK;
    }
}
EOL

    # Create a symbolic link to enable the blog site
    sudo ln -s /etc/nginx/sites-available/blog /etc/nginx/sites-enabled/
    echo "Nginx site configuration for the blog has been created and enabled."

    # Add the user to the www-data group
    sudo gpasswd -a www-data $USERNAME
    echo "User $USERNAME has been added to the www-data group."
  else
    echo "Operation cancelled."
    exit 1
  fi
}

# Function to restart services
restart_services() {
  sudo systemctl start gunicorn.socket
  sudo systemctl enable gunicorn.socket
  sudo systemctl restart nginx
  sudo service gunicorn restart
  sudo service nginx restart
  echo "Nginx and Gunicorn have been restarted."
}

# Run all setup functions
setup_gunicorn_socket
setup_gunicorn_service
setup_nginx
restart_services
