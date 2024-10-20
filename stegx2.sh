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

# Get the directory where the script is executed (assumed to be inside the SD card)
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

# Main function to handle extraction
extract_text_from_jpg() {
    select_jpg

    # Ask for the password
    read -sp "Enter the password for the selected steganographic JPG file: " password
    echo

    # Define output text file name based on JPG file name
    output_file="${jpgfile%.*}.txt"

    # Extract the hidden text using stegosuite
    # Redirect output to the .txt file
    stegosuite extract -k "$password" "$jpgfile" > "$output_file"

    # Check if extraction was successful
    if [ $? -eq 0 ]; then
        echo "Hidden text extracted and saved to $output_file"
    else
        echo "Failed to extract hidden text. Please check the password or file."
        rm -f "$output_file"  # Clean up the output file if extraction fails
    fi
}

# Menu function to select next steps
menu() {
    echo
    echo "What would you like to do next?"
    echo "1) Extract hidden text from another JPG file"
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

# Main menu function to run extraction and display menu options afterward
main_menu() {
    extract_text_from_jpg
    menu
}

# Start the script by checking if Stegosuite is installed and show the main menu if installed
check_install_stegosuite
main_menu
