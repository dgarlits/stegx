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
        self.master.configure(bg='black')  # Change GUI background color to black
        self.selected_file = None
        self.image_label = None  # To hold the image label

        # Layout configuration
        self.left_frame = tk.Frame(master, bg='black')  # Set left frame background to black
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.right_frame = tk.Frame(master, bg='black')  # Set right frame background to black
        self.right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # File selection button
        self.select_button = tk.Button(self.left_frame, text="Select File", command=self.select_file)
        self.select_button.pack()

        # Display selected file name
        self.file_name_label = tk.Label(self.left_frame, text="Selected file:", bg='black', fg='white')  # Label background black, text white
        self.file_name_label.pack()

        # Image preview
        self.image_label = tk.Label(self.left_frame, bg='black')  # Initialize the label for the image with black background
        self.image_label.pack()

        # Font size input
        self.font_size_label = tk.Label(self.left_frame, text="Font Size (12-22):", bg='black', fg='white')  # Label background black, text white
        self.font_size_label.pack()
        self.font_size_entry = tk.Entry(self.left_frame)
        self.font_size_entry.pack()

        # Password entry
        self.password_label = tk.Label(self.left_frame, text="Password:", bg='black', fg='white')  # Label background black, text white
        self.password_label.pack()
        self.password_entry = tk.Entry(self.left_frame, show="*")
        self.password_entry.pack()

        # Extract text button
        self.extract_button = tk.Button(self.left_frame, text="Extract Text", command=self.extract_text)
        self.extract_button.pack()

        # Text display area
        self.text_display = tk.Text(self.right_frame, wrap=tk.WORD, height=20, width=50, bg='#2E2E2E')  # Change text display box background color
        self.text_display.pack()

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
            img.thumbnail((150, 150))  # Resize image for preview
            self.img_tk = ImageTk.PhotoImage(img)  # Convert to PhotoImage
            self.image_label.config(image=self.img_tk)  # Update label with the image
            se
