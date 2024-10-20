#!/usr/bin/env python3

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import subprocess

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Text Extractor")
        self.selected_file = None

        # Layout configuration
        self.left_frame = tk.Frame(master)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.right_frame = tk.Frame(master)
        self.right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # File selection button
        self.select_button = tk.Button(self.left_frame, text="Select File", command=self.select_file)
        self.select_button.pack()

        # Display selected file name
        self.file_name_label = tk.Label(self.left_frame, text="Selected file:")
        self.file_name_label.pack()

        # Font size input
        self.font_size_label = tk.Label(self.left_frame, text="Font Size (12-22):")
        self.font_size_label.pack()
        self.font_size_entry = tk.Entry(self.left_frame)
        self.font_size_entry.pack()

        # Password entry
        self.password_label = tk.Label(self.left_frame, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.left_frame, show="*")
        self.password_entry.pack()

        # Extract text button
        self.extract_button = tk.Button(self.left_frame, text="Extract Text", command=self.extract_text)
        self.extract_button.pack()

        # Text display area
        self.text_display = tk.Text(self.right_frame, wrap=tk.WORD, height=20, width=50)
        self.text_display.pack()

    def select_file(self):
        filetypes = [('JPEG Files', '*.jpg'), ('All Files', '*.*')]
        self.selected_file = filedialog.askopenfilename(title="Select a JPG file", filetypes=filetypes)
        if self.selected_file:
            self.file_name_label.config(text=f"Selected file: {os.path.basename(self.selected_file)}")

    def extract_text(self):
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a file first.")
            return

        password = self.password_entry.get()  # Get the password from the entry field
        output_file = f"{os.path.splitext(self.selected_file)[0]}.txt"

        # Use Stegosuite for extraction (replace with actual extraction logic)
        process = subprocess.run(['stegosuite', 'extract', '-k', password, self.selected_file], capture_output=True, text=True)

        if process.returncode == 0:
            # Check if the output file was created
            if os.path.exists(output_file):
                with open(output_file, 'r') as f:
                    extracted_text = f.read()  # Read the extracted text from the file

                try:
                    font_size = int(self.font_size_entry.get())
                    if font_size < 12 or font_size > 22:
                        raise ValueError("Font size must be between 12 and 22.")
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
                    return

                # Display extracted text in the text display area
                self.text_display.config(font=('Arial', font_size))
                self.text_display.delete(1.0, tk.END)  # Clear existing text
                self.text_display.insert(tk.END, extracted_text)  # Insert new text
            else:
                messagebox.showerror("Error", "No extracted text file found.")
        else:
            messagebox.showerror("Error", f"Failed to extract text: {process.stderr}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
