#!/bin/bash

application_name="nexus_fusion"
application_folder_name="iotlimsintegrator"
application_path="/home/$USER/${application_name}"
PROJECT_DIR="/home/ubuntu/nexus_fusion/iotlimsintegrator"
GUNICORN_SOCK="/run/gunicorn.sock"
GUNICORN_APP="iotlimsintegrator.wsgi:application"

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
User=$USER
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
    sudo tee /etc/nginx/sites-available/nexus_fusion <<EOL
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
    sudo ln -s /etc/nginx/sites-available/nexus_fusion /etc/nginx/sites-enabled/
    echo "Nginx site configuration for the blog has been created and enabled."

    # Add the user to the www-data group
    sudo gpasswd -a www-data $USER
    echo "User $USER has been added to the www-data group."
  else
    echo "Operation cancelled."
    exit 1
  fi
}

execute_python_services() {
  #Project migration and static files handling
  source ${application_path}/${application_folder_name}/env/bin/activate
  python ${application_path}/${application_folder_name}/manage.py makemigrations
  python ${application_path}/${application_folder_name}/manage.py migrate
  python ${application_path}/${application_folder_name}/manage.py collectstatic

  read -p "Do you want to create superuser? (yes/no): " confirm
  if [ "$confirm" == "yes" ]; then
    python ${application_path}/${application_folder_name}/manage.py createsuperuser
  fi
  deactivate
}

configure_celery() {
  sudo apt install -y supervisor

  if [ ! -d "/var/log/celery/" ]; then
    # Create the directory
    sudo mkdir -p "/var/log/celery/"
  fi

  cat <<EOL | sudo tee /etc/supervisor/conf.d/celery_worker.conf
[program:celery_worker]
command=${application_path}/${application_folder_name}/env/bin/celery -A ${application_folder_name} worker --loglevel=info -E
directory=${application_path}/${application_folder_name}
user=$USER
autostart=true
autorestart=true
stopasgroup=true
stdout_logfile=/var/log/celery/worker.log
stderr_logfile=/var/log/celery/worker_error.log
EOL

  cat <<EOL | sudo tee /etc/supervisor/conf.d/celery_beat.conf
[program:celery_beat]
command=${application_path}/${application_folder_name}/env/bin/celery -A ${application_folder_name} beat --loglevel=info
directory=${application_path}/${application_folder_name}
user=$USER
autostart=true
autorestart=true
stopasgroup=true
stdout_logfile=/var/log/celery/beat.log
stderr_logfile=/var/log/celery/beat_error.log
EOL

  sudo supervisorctl reread
  sudo supervisorctl update

}

# Function to restart services
restart_services() {
  sudo systemctl start gunicorn.socket
  sudo systemctl enable gunicorn.socket
  sudo systemctl restart redis-server
  sudo systemctl enable redis-server
  sudo systemctl status redis-server
  sudo systemctl restart nginx
  sudo service gunicorn restart
  sudo service nginx restart
  sudo supervisorctl restart celery_worker
  sudo supervisorctl restart celery_beat
  sudo supervisorctl status
  sudo systemctl status nginx
  echo "All the required services have been restarted."
}

# Run all setup functions
setup_gunicorn_socket
setup_gunicorn_service
setup_nginx
execute_python_services
configure_celery
restart_services
