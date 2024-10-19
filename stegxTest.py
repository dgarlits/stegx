#!/usr/bin/env python3

import os
import subprocess
from tkinter import filedialog, messagebox, Tk, Label, Button, Entry, Text, Scrollbar, Frame
from tkinter.constants import BOTH, END, VERTICAL, HORIZONTAL, WORD

# Function to check if Stegosuite is installed
def check_stegosuite_installed():
    try:
        subprocess.run(["stegosuite", "--help"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        messagebox.showerror("Error", "Stegosuite is not installed. Please install it first.")
        return False
    return True

# Function to select JPG file
def select_jpg():
    jpgfile = filedialog.askopenfilename(title="Select JPG File", filetypes=[("JPG Files", "*.jpg")])
    if jpgfile:
        selected_file_label.config(text=f"Selected file: {jpgfile}")
    return jpgfile

# Function to save extracted text
def save_extracted_text(default_name, text_content):
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=default_name)
    if save_path:
        with open(save_path, "w") as file:
            file.write(text_content)
        messagebox.showinfo("Success", f"Text saved to {save_path}")

# Function to extract hidden text from the selected JPG
def extract_text():
    if not check_stegosuite_installed():
        return
    
    jpgfile = select_jpg()
    if not jpgfile:
        messagebox.showerror("Error", "No file selected.")
        return

    password = password_entry.get()
    if not password:
        messagebox.showerror("Error", "Password is required.")
        return

    try:
        # Run Stegosuite command to extract text
        result = subprocess.run(
            ["stegosuite", "extract", "-k", password, jpgfile],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if result.returncode == 0:
            extracted_text = result.stdout.decode()

            # Display the extracted text in the text area
            text_display.delete(1.0, END)
            text_display.insert(END, extracted_text)

            # Enable the save button after successful extraction
            save_button.config(state="normal")
        else:
            error_msg = result.stderr.decode() or "Unknown error"
            messagebox.showerror("Error", f"Failed to extract hidden text: {error_msg}")

    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Extraction failed: {e.stderr.decode()}")

# GUI setup with dark theme
def create_gui():
    global root, password_entry, text_display, selected_file_label, save_button

    root = Tk()
    root.title("StegX")
    root.configure(bg="#2e2e2e")  # Dark background
    root.geometry("800x600")

    # File selection frame
    file_frame = Frame(root, bg="#2e2e2e")
    file_frame.pack(fill="x", padx=10, pady=10)

    selected_file_label = Label(file_frame, text="No file selected", fg="#ffffff", bg="#2e2e2e")
    selected_file_label.pack()

    select_file_button = Button(file_frame, text="Select JPG File", command=select_jpg, bg="#565656", fg="#ffffff")
    select_file_button.pack(pady=5)

    # Password input frame
    password_frame = Frame(root, bg="#2e2e2e")
    password_frame.pack(fill="x", padx=10, pady=10)

    Label(password_frame, text="Enter Password:", fg="#ffffff", bg="#2e2e2e").pack(side="left")
    password_entry = Entry(password_frame, show="*", bg="#3c3c3c", fg="#ffffff", insertbackground="white")
    password_entry.pack(side="left", padx=10, pady=5)

    # Extract button
    extract_button = Button(root, text="Extract file", command=extract_text, bg="#565656", fg="#ffffff")
    extract_button.pack(pady=10)

    # Text display frame
    text_frame = Frame(root, bg="#2e2e2e")
    text_frame.pack(fill="both", expand=True, padx=10, pady=10)

    text_display = Text(text_frame, wrap=WORD, bg="#3c3c3c", fg="#ffffff", width=80, height=20)
    text_display.pack(fill="both", expand=True, padx=5, pady=5)

    # Scrollbar for the text display
    scrollbar = Scrollbar(text_frame, command=text_display.yview, bg="#2e2e2e")
    text_display.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill=VERTICAL)

    # Save button
    save_button = Button(root, text="Save Extracted Text", state="disabled", command=lambda: save_extracted_text("extracted_text.txt", text_display.get(1.0, END)), bg="#565656", fg="#ffffff")
    save_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
