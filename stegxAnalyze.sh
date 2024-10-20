#!/bin/bash

# Function to check and install Stegosuite if it's not installed
check_install_stegosuite() {
    if ! command -v stegosuite &> /dev/null; then
        echo "Stegosuite is not installed."
        read -p "Would you like to install it now? (y/n): " install_choice
        if [[ "$install_choice" == "y" || "$install_choice" == "Y" ]]; then
            sudo apt update
            sudo apt install stegosuite -y
            if [ $? -eq 0 ]; then
                echo "Stegosuite installed successfully."
                return 0  # Continue to the main menu
            else
                echo "Failed to install Stegosuite. Exiting..."
                exit 1
            fi
        else
            echo "Exiting..."
            exit 1
        fi
    fi
}

# Clear the screen
clear

# Get the directory where the script is executed
WORK_DIR=$(pwd)

# Function to list JPG files and allow the user to select one
select_jpg() {
    echo "Available JPG files in $WORK_DIR:"
    select jpgfile in *.jpg; do
        if [[ -n "$jpgfile" ]]; then
            echo "You selected: $jpgfile"
            break
        else
            echo "Invalid selection, please try again."
        fi
    done
}

# Main function to check the capacity of the selected JPG file
check_capacity_of_jpg() {
    select_jpg

    # Run the StegoSuite capacity command
    echo "Analyzing capacity for $jpgfile..."
    capacity_output=$(stegosuite capacity "$jpgfile")

    # Check if the command was successful and display the capacity
    if [ $? -eq 0 ]; then
        echo "$capacity_output"
    else
        echo "Failed to analyze capacity for $jpgfile. Please check the file."
    fi
}

# Menu function to select next steps
menu() {
    echo
    echo "What would you like to do next?"
    echo "1) Check capacity of another JPG file"
    echo "2) Quit"
    read -p "Select an option (1 or 2): " choice

    case "$choice" in
        1)
            clear
            main_menu  # Show the main menu again
            ;;
        2)
            echo "Goodbye!"
            exit 0
            ;;
        *)
            echo "Invalid option. Please select 1 or 2."
            menu
            ;;
    esac
}

# Main menu function to check capacity and display menu options afterward
main_menu() {
    check_capacity_of_jpg
    menu
}

# Start the script by checking if Stegosuite is installed and showing the main menu if installed
check_install_stegosuite
main_menu
