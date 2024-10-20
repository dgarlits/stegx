#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

class StegoSuiteGUI:
    def __init__(self, master):
        self.master = master
        master.title("StegoSuite GUI")

        # Image File Label and Entry
        self.image_label = tk.Label(master, text="JPG File:")
        self.image_label.grid(row=0, column=0)

        self.image_entry = tk.Entry(master)
        self.image_entry.grid(row=0, column=1)

        self.image_button = tk.Button(master, text="Browse", command=self.browse_image)
        self.image_button.grid(row=0, column=2)

        # Password Label and Entry
        self.password_label = tk.Label(master, text="Password:")
        self.password_label.grid(row=1, column=0)

        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.grid(row=1, column=1)

        # Run Button
        self.run_button = tk.Button(master, text="Extract Hidden Text", command=self.extract_hidden_text)
        self.run_button.grid(row=2, column=1)

        # Check if Stegosuite is installed
        self.check_install_stegosuite()

    def browse_image(self):
        filename = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg")])
        self.image_entry.delete(0, tk.END)
        self.image_entry.insert(0, filename)

    def extract_hidden_text(self):
        jpg_file = self.image_entry.get()
        password = self.password_entry.get()

        if not jpg_file or not password:
            messagebox.showerror("Input Error", "Please fill all fields")
            return

        # Define output file name
        output_file = os.path.splitext(jpg_file)[0] + ".txt"

        # Prepare the command to run the Bash script
        command = f"stegosuite extract -k '{password}' '{jpg_file}' > '{output_file}'"
        
        try:
            subprocess.run(command, shell=True, check=True)
            messagebox.showinfo("Success", f"Hidden text extracted and saved to {output_file}")
        except subprocess.CalledProcessError:
            messagebox.showerror("Execution Error", "Failed to extract hidden text. Please check the password or file.")

    def check_install_stegosuite(self):
        try:
            subprocess.run("command -v stegosuite", shell=True, check=True, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError:
            install_choice = messagebox.askyesno("Install Stegosuite", "Stegosuite is not installed. Would you like to install it now?")
            if install_choice:
                self.install_stegosuit
