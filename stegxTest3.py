#!/usr/bin/env python3

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import subprocess

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("StegX - Frontend for Stegosuite")
        self.selected_file = None
        self.image_label = None  # To hold the image label

        # Layout configuration
        self.left_frame = tk.Frame(master, bg='#000026')  # Set left frame background
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.right_frame = tk.Frame(master, bg='#000026')  # Set right frame background
        self.right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # File selection button
        self.select_button = tk.Button(self.left_frame, text="Select File", command=self.select_file, bg='#000026', fg='white')
        self.select_button.pack()

        # Display selected file name
        self.file_name_label = tk.Label(self.left_frame, text="Selected file:", bg='#000026', fg='white')
        self.file_name_label.pack()

        # Image preview
        self.image_label = tk.Label(self.left_frame, bg='#2E2E2E')  # Initialize the label for the image
        self.image_label.pack()

        # Font size input
        self.font_size_label = tk.Label(self.left_frame, text="Font Size (12-22):", bg='#000026', fg='white')
        self.font_size_label.pack()
        self.font_size_entry = tk.Entry(self.left_frame, bg='#000026', fg='white')  # Change entry box background and text color
        self.font_size_entry.pack()

        # Password entry
        self.password_label = tk.Label(self.left_frame, text="Password:", bg='#000026', fg='white')
        self.password_label.pack()
        self.password_entry = tk.Entry(self.left_frame, show="*", bg='#000026', fg='white')  # Change entry box background and text color
        self.password_entry.pack()

        # Extract text button
        self.extract_button = tk.Button(self.left_frame, text="Extract Text", command=self.extract_text, bg='#000026', fg='white')
        self.extract_button.pack()

        # Text display area
        self.text_display = tk.Text(self.right_frame, wrap=tk.WORD, height=20, width=50, bg='#2E2E2E', fg='white')  # Change text display box background and text color
        self.text_display.pack()

        # Change GUI background color to #000026
        master.configure(bg='#000026')

    def select_file(self):
        filetypes = [('JPEG Files', '*.jpg'), ('All Files', '*.*')]
        self.selected_file = filedialog.askopenfilename(title="Select a JPG file", filetypes=filetypes)
        if self.selected_file:
            self.file_name_label.config(text=f"Selected file: {os.path.basename(self.selected_file)}")
            self.display_image(self.selected_file)  # Call to display the image

    def display_image(self, file_path):
        try:
            # Open the image file
            img = Image.open(file_path)
            img.thumbnail((300, 300))  # Resize image for preview
            self.img_tk = ImageTk.PhotoImage(img)  # Convert to PhotoImage
            self.image_label.config(image=self.img_tk)  # Update label with the image
            self.image_label.image = self.img_tk  # Keep a reference to avoid garbage collection
        except Exception as e:
            messagebox.showerror("Error", f"Could not display image: {e}")
            
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
                self.text_display.config(font=('Arial', font_size), fg="white")
                self.text_display.delete(1.0, tk.END)  # Clear existing text
                self.text_display.insert(tk.END, extracted_text)  # Insert new text
            else:
                messagebox.showerror("Error", "No extracted text file found. Please check if Stegosuite outputs to a different location.")
                print(f"Expected output file: {output_file}")
                print(f"Current working directory: {os.getcwd()}")
                print(process.stdout)  # Show standard output for debugging
                print(process.stderr)   # Show standard error for debugging
        else:
            messagebox.showerror("Error", f"Failed to extract text: {process.stderr}")
            print(process.stderr)  # Output error details for debugging



if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
