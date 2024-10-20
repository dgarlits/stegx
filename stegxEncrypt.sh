#!/bin/bash

# Check if StegoSuite is installed
if ! command -v stegosuite &> /dev/null; then
    echo "StegoSuite is not installed. Please install it to proceed."
    exit 1
fi

# Function to prompt user to select a .txt file
select_txt_file() {
    echo "Please select a .txt file to encrypt:"
    select file in *.txt; do
        if [ -n "$file" ]; then
            echo "You selected: $file"
            break
        else
            echo "Invalid selection. Please try again."
        fi
    done
    echo "$file"
}

# Function to prompt user to select a .jpg file
select_jpg_file() {
    echo "Please select a .jpg file to use as a cover image:"
    select file in *.jpg; do
        if [ -n "$file" ]; then
            echo "You selected: $file"
            break
        else
            echo "Invalid selection. Please try again."
        fi
    done
    echo "$file"
}

# Main script execution
txt_file=$(select_txt_file)
jpg_file=$(select_jpg_file)

# Prompt for password
read -s -p "Enter a password for encryption: " password
echo
read -s -p "Confirm the password: " password_confirm
echo

# Check if passwords match
if [ "$password" != "$password_confirm" ]; then
    echo "Passwords do not match. Exiting."
    exit 1
fi

# Prompt for output filename
read -p "Enter the output filename (without extension): " output_name
output_file="${output_name}.jpg"

# Encrypt the .txt file into the .jpg file using StegoSuite
stegosuite -e "$txt_file" "$jpg_file" -o "$output_file" -p "$password"

echo "Encryption complete! The file has been saved as $output_file."
