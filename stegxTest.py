#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import subprocess
import os

# Function to extract hidden text using stegosuite
def extract_text_from_jpg(image_path, password):
    try:
        # Command to extract the hidden text from the image
        output_file = f"{os.path.splitext(image_path)[0]}.txt"
        cmd = ['stegosuite', 'extract', '-k', password, image_path]
        
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            return result.stdout.strip()  # Return extracted text
        else:
            raise Exception(f"Stegosuite failed: {result.stderr.strip()}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to extract hidden text: {str(e)}")
        return None

# Function to handle file selection
def select_file():
    filetypes = [('JPEG Files', '*.jpg'), ('All Files', '*.*')]
    file_path = filedialog.askopenfilename(title="Select a JPG file", filetypes=filetypes)
    if file_path:
        try:
            # Load and display image
            img = Image.open(file_path)
            img.thumbnail((300, 300))  # Resize image to fit GUI window
            img_tk = ImageTk.PhotoImage(img)
            img_label.config(image=img_tk)
            img_label.image = img_tk  # Keep a reference to prevent garbage collection
            selected_file.set(file_path)  # Update selected file path
        except Exception as e:
            messagebox.showerror("Error", f"Unable to open image: {str(e)}")

# Function to extract text and display it in a text box
def extract_and_display_text():
    file_path = selected_file.get()
    password = password_entry.get()

    if not file_path or not password:
        messagebox.showwarning("Missing Input", "Please select a file and enter a password.")
        return

    extracted_text = extract_text_from_jpg(file_path, password)
    if extracted_text:
        text_display.delete(1.0, tk.END)  # Clear previous content
        text_display.insert(tk.END, extracted_text)

# Function to save the extracted text
def save_text():
    extracted_text = text_display.get(1.0, tk.END).strip()
    if not extracted_text:
        messagebox.showwarning("No Text", "There is no extracted text to save.")
        return

    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if save_path:
        with open(save_path, 'w') as f:
            f.write(extracted_text)
        messagebox.showinfo("Saved", f"Extracted text saved to {save_path}")

# Create main application window
root = tk.Tk()
root.title("StegX")

# Set a dark theme for the GUI
root.configure(bg='#2e2e2e')
root.geometry("600x500")

# Variable to store the selected file path
selected_file = tk.StringVar()

# Label and button to select the file
file_select_btn = tk.Button(root, text="Select JPG File", command=select_file, bg='#444', fg='white')
file_select_btn.pack(pady=10)

img_label = tk.Label(root, bg='#2e2e2e')
img_label.pack(pady=10)

# Password entry box
password_label = tk.Label(root, text="Enter Password:", bg='#2e2e2e', fg='white')
password_label.pack(pady=5)
password_entry = tk.Entry(root, show='*', width=40)
password_entry.pack(pady=5)

# Button to extract text
extract_btn = tk.Button(root, text="Extract Text", command=extract_and_display_text, bg='#444', fg='white')
extract_btn.pack(pady=10)

# Scrolled text box to display extracted text
text_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20, bg='#1e1e1e', fg='white', insertbackground='white')
text_display.pack(pady=10)

# Button to save the extracted text
save_btn = tk.Button(root, text="Save Extracted Text", command=save_text, bg='#444', fg='white')
save_btn.pack(pady=10)

root.mainloop()
