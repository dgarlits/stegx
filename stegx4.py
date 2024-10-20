#!/usr/bin/env python3

import os
import tkinter as tk
from tkinter import filedialog, messagebox, font as tkfont
from PIL import Image, ImageTk
import subprocess

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("StegX - Frontend for Stegosuite")
        self.selected_file = None

        # Layout configuration
        self.left_frame = tk.Frame(master, bg='#000026')
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.right_frame = tk.Frame(master, bg='#000026')
        self.right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # File selection button
        self.select_button = tk.Button(self.left_frame, text="Select File", command=self.select_file, bg='#000026', fg='white')
        self.select_button.pack()

        # Display selected file name
        self.file_name_label = tk.Label(self.left_frame, text="Selected file:", bg='#000026', fg='white')
        self.file_name_label.pack()

        # Image preview
        self.image_label = tk.Label(self.left_frame, bg='#2E2E2E')
        self.image_label.pack()

        # Password entry
        self.password_label = tk.Label(self.left_frame, text="Password:", bg='#000026', fg='white')
        self.password_label.pack()
        self.password_entry = tk.Entry(self.left_frame, show="*", bg='#000026', fg='white')
        self.password_entry.pack()

        # Extract text button
        self.extract_button = tk.Button(self.left_frame, text="Extract Text", command=self.extract_text, bg='#000026', fg='white')
        self.extract_button.pack()

        # Text display area with font control
        self.text_display = tk.Text(self.right_frame, wrap=tk.WORD, height=20, width=50, bg='#2E2E2E', fg='white', font=tkfont.Font(family="Helvetica", size=12))
        self.text_display.pack()

        # Change GUI background color to #000026
        master.configure(bg='#000026')

    def select_file(self):
        filetypes = [('JPEG Files', '*.jpg'), ('All Files', '*.*')]
        self.selected_file = filedialog.askopenfilename(title="Select a JPG file", filetypes=filetypes)
        if self.selected_file:
            self.file_name_label.config(text=f"Selected file: {os.path.basename(self.selected_file)}")
            self.display_image(self.selected_file)

    def display_image(self, file_path):
        try:
            img = Image.open(file_path)
            img.thumbnail((300, 300))  # Resize image for preview
            self.img_tk = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.img_tk)
            self.image_label.image = self.img_tk
        except Exception as e:
            messagebox.showerror("Error", f"Could not display image: {e}")

    def extract_text(self):
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a file first.")
            return

        password = self.password_entry.get()
        output_file = f"{os.path.splitext(self.selected_file)[0]}.txt"

        # Construct the command as a single string
        command = f'stegosuite extract -k "{password}" "{self.selected_file}"'
        
        try:
            # Use subprocess to run the command directly
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to extract text: {e}")
            return

        # Check if the output file exists and display its contents
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                extracted_text = f.read()

            self.text_display.delete(1.0, tk.END)  # Clear the text box
            self.text_display.insert(tk.END, extracted_text)  # Insert the extracted text
        else:
            messagebox.showerror("Error", f"No text file found. Expected: {output_file}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
