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
        self.text_display
