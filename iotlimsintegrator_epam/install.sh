#!/bin/bash


SCRIPT1="./scripts/setup_env.sh"
SCRIPT2="./scripts/create_services.sh"

while true; do
    echo "Please choose an option:"
    echo "1) Continue with Environment setup."
    echo "2) Continue with Service creation"
    echo "3) Exit"
    read -p "Enter your choice [1-3]: " choice

    case $choice in
        1)
            echo "Processing the script for Environment setup..."
            $SCRIPT1
            if [ $? -ne 0 ]; then
                echo "Script execution failed."
            else
                echo "Environment setup is successfully completed."
            fi
            ;;
        2)
            echo "Processing the script for Service creation..."
            $SCRIPT2
            if [ $? -ne 0 ]; then
                echo "script execution failed."
            else
                echo "Service creation is successfully completed."
            fi
            ;;
        3)
            echo "Exiting..."
            break
            ;;
        *)
            echo "Invalid option. Please choose 1, 2, or 3."
            ;;
    esac
    # Prompt to ask if the user wants to continue
    read -p "Do you want to continue? (yes/no): " continue_choice
    case $continue_choice in
        [Yy]* )
            clear
            ;;
        [Nn]* )
            echo "Exiting..."
            break
            ;;
        * )
            echo "Invalid input. Exiting..."
            break
            ;;
    esac
done