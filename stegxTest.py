#!/usr/bin/env python3

import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk  # Pillow is needed for image preview
import sys

# Function to check if Stegosuite is installed
def check_stegosuite():
    try:
        subprocess.run(["stegosuite", "--version"], check=True)
    except subprocess.CalledProcessError:
        return False
    return True

# Function to extract text from a selected JPG file
def extract_text(jpgfile, password):
    output_file = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")],
        title="Save extracted text as"
    )

    if not output_file:
        return  # User cancelled the save dialog

    try:
        result = subprocess.run(
            ["stegosuite", "extract", "-k", password, jpgfile],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Print output for debugging
        print("STDOUT:", result.stdout.decode())
        print("STDERR:", result.stderr.decode())

        if result.returncode == 0 and os.path.exists(output_file):
            messagebox.showinfo("Success", f"Hidden text extracted and saved to {output_file}")
        else:
            error_msg = result.stderr.decode() if result.stderr else "No error message available."
            messagebox.showerror("Error", f"Failed to extract hidden text:\n{error_msg}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

# Function to open file dialog and select a JPG file
def select_jpg():
    jpgfile = filedialog.askopenfilename(
        title="Select a JPG file",
        filetypes=[("JPG files", "*.jpg")]
    )
    if jpgfile:
        display_image(jpgfile)  # Show the selected image
        jpg_label.config(text=os.path.basename(jpgfile))  # Show the filename
        jpg_label.file_path = jpgfile  # Store the file path for extraction

# Function to display the selected image in the GUI
def display_image(jpgfile):
    img = Image.open(jpgfile)
    img.thumbnail((300, 300))  # Resize image for preview
    img_tk = ImageTk.PhotoImage(img)

    # Clear previous image and set new image
    image_label.config(image=img_tk)
    image_label.image = img_tk  # Keep a reference to avoid garbage collection

    # Resize the window based on the image size
    root.geometry(f"{img.width + 40}x{img.height + 200}")  # Add padding for other UI elements
    root.update_idletasks()  # Update the window to reflect changes

# Function to run the extraction process
def run_extraction():
    try:
        jpgfile = jpg_label.file_path  # Get the filename from the label
        if not jpgfile:
            messagebox.showwarning("Warning", "Please select a JPG file.")
            return  # No file selected

        password = password_entry.get()  # Get password from entry field
        if not password:
            messagebox.showwarning("Warning", "Please enter the password.")
            return  # No password entered

        extract_text(jpgfile, password)
    except AttributeError:
        messagebox.showwarning("Warning", "Please select a JPG file first.")

# Function to create the main application window
def main():
    if not check_stegosuite():
        if messagebox.askyesno("Stegosuite Not Found", "Stegosuite is not installed. Would you like to install it now?"):
            subprocess.run(["sudo", "apt", "install", "stegosuite", "-y"])
            if not check_stegosuite():
                messagebox.showerror("Installation Failed", "Failed to install Stegosuite. Exiting.")
                sys.exit(1)

    global root, image_label, password_entry, jpg_label
    root = tk.Tk()
    root.title("Stegosuite Extractor")
    root.geometry("400x450")  # Set initial size
    root.configure(bg="#f0f0f0")  # Background color

    # Create a title label
    title_label = tk.Label(root, text="Stegosuite Extractor", font=("Arial", 16, "bold"), bg="#f0f0f0")
    title_label.pack(pady=10)

    # Image label for preview
    image_label = tk.Label(root, bg="#ffffff", relief=tk.SUNKEN)
    image_label.pack(pady=10, padx=10)

    # Label to display selected JPG file
    jpg_label = tk.Label(root, text="No file selected", bg="#f0f0f0", fg="#555555")
    jpg_label.pack(pady=5)
    jpg_label.file_path = None  # Initialize file_path

    # Password entry
    password_label = tk.Label(root, text="Enter Password:", bg="#f0f0f0")
    password_label.pack(pady=5)

    password_entry = tk.Entry(root, show='*', width=30)
    password_entry.pack(pady=5)

    # Create buttons
    select_button = tk.Button(root, text="Select JPG File", command=select_jpg, bg="#2196F3", fg="white")
    select_button.pack(pady=5)

    extract_button = tk.Button(root, text="Extract Text from JPG", command=run_extraction, bg="#4CAF50", fg="white")
    extract_button.pack(pady=20)

    exit_button = tk.Button(root, text="Exit", command=root.quit, bg="#f44336", fg="white")
    exit_button.pack(pady=5)

    root.mainloop()  # Start the GUI event loop

if __name__ == "__main__":
    main()
