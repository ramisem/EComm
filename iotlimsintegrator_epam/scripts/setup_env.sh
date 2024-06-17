#!/bin/bash

setup_application_name="nexus_fusion"
setup_application_folder_name="iotlimsintegrator"
setup_application_path="/home/$USER/${setup_application_name}"

# Prompt for user input
read -p "Enter the Python version to install (e.g., 3.8): " PYTHON_VERSION

read -p "Do you want to install python${PYTHON_VERSION} and create the virtual environment? (yes/no): " confirm
if [ "$confirm" == "yes" ]; then
  # Add the deadsnakes PPA for Python
  sudo add-apt-repository ppa:deadsnakes/ppa

  # Install Python, its development files, virtual environment package, and nginx
  sudo apt install -y python${PYTHON_VERSION} python${PYTHON_VERSION}-dev python${PYTHON_VERSION}-venv nginx

  # Download get-pip.py script
  curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

  # Install pip for the specified Python version
  sudo python${PYTHON_VERSION} get-pip.py

  # Install virtualenv using pip
  python${PYTHON_VERSION} -m pip install virtualenv

  sudo apt install net-tools

  python${PYTHON_VERSION} -m virtualenv ${setup_application_path}/${setup_application_folder_name}/env

  sudo apt-get install redis-server -y
fi

read -p "Do you want to install the latest version of the application? (yes/no): " confirm
if [ "$confirm" == "yes" ]; then
  if [ ! -d "${setup_application_path}/${setup_application_folder_name}/" ]; then
    # Create the directory
    mkdir -p "${setup_application_path}/${setup_application_folder_name}/"
  fi
  unzip $PWD/iotlimsintegrator.zip -d ${setup_application_path}/${setup_application_folder_name}/
fi

read -p "Do you want to install required Python Packages? (yes/no): " confirm
if [ "$confirm" == "yes" ]; then
  source ${setup_application_path}/${setup_application_folder_name}/env/bin/activate
  pip install -r ${setup_application_path}/${setup_application_folder_name}/requirements.txt
  pip install django gunicorn
fi

read -p "Do you want to install 'PostgreSQL? (yes/no): " confirm
if [ "$confirm" == "yes" ]; then
  sudo sh -c 'echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
  wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
  sudo apt-get update
  sudo apt-get -y install postgresql-15
  sudo service postgresql status
fi

read -p "Do you want to update the password for 'postgres' user? (yes/no): " confirm
if [ "$confirm" == "yes" ]; then
  read -sp "Enter the new password for the postgres user: " NEW_PASSWORD
  echo
  # Switch to the postgres user and execute the psql commands
  sudo -i -u postgres bash <<EOF
psql -c "ALTER USER postgres WITH PASSWORD '$NEW_PASSWORD';"
psql -c "\\du"
EOF
fi
