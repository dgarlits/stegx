#!/bin/bash

# Ensure Stegosuite is installed
if ! command -v stegosuite &> /dev/null; then
    echo "Stegosuite is not installed. Please install it first."
    exit 1
fi

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

# Run the extraction function
extract_text_from_jpg
