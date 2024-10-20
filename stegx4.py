#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import os
from PIL import Image, ImageTk

class StegoSuiteGUI:
    def __init__(self, master):
        self.master = master
        master.title("StegoSuite GUI")

        # Image File Label and Entry
        self.image_label = tk.Label(master, text="Select JPG File:")
        self.image_label.grid(row=0, column=0)

        self.image_entry = tk.Entry(master)
        self.image_entry.grid(row=0, column=1)

        self.image_button = tk.Button(master, text="Browse", command=self.browse_image)
        self.image_button.grid(row=0, column=2)

        # Thumbnail Label
        self.thumbnail_label = tk.Label(master)
        self.thumbnail_label.grid(row=1, column=0, columnspan=3, pady=10)

        # Password Label and Entry
        self.password_label = tk.Label(master, text="Password:")
        self.password_label.grid(row=2, column=0)

        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.grid(row=2, column=1)

        # Extract Button
        self.extract_button = tk.Button(master, text="Extract", command=self.extract_hidden_text)
        self.extract_button.grid(row=3, column=1)

        # Read Button
        self.read_button = tk.Button(master, text="Read", command=self.read_hidden_text)
        self.read_button.grid(row=3, column=2)

        # Text Box for Displaying Extracted Text
        self.text_box = scrolledtext.ScrolledText(master, width=100, height=20)
        self.text_box.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        # Check if Stegosuite is installed
        self.check_install_stegosuite()

    def browse_image(self):
        filename = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg")])
        self.image_entry.delete(0, tk.END)
        self.image_entry.insert(0, filename)
        self.show_thumbnail(filename)

    def show_thumbnail(self, file_path):
        try:
            img = Image.open(file_path)
            img.thumbnail((300, 300), Image.LANCZOS)  # Use Image.LANCZOS for high-quality resizing
            self.thumbnail = ImageTk.PhotoImage(img)
            self.thumbnail_label.config(image=self.thumbnail)
        except Exception as e:
            messagebox.showerror("Image Error", f"Could not open image: {e}")

    def extract_hidden_text(self):
        jpg_file = self.image_entry.get()
        password = self.password_entry.get()

        if not jpg_file or not password:
            messagebox.showerror("Input Error", "Please fill all fields")
            return

        # Define output file name
        output_file = os.path.splitext(jpg_file)[0] + ".txt"

        # Prepare the command to run the extraction
        command = f"stegosuite extract -k '{password}' '{jpg_file}' > '{output_file}' 2>&1"

        try:
            # Execute the command
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)

            # Check if the output file was created
            if os.path.exists(output_file):
                messagebox.showinfo("Success", f"Hidden text extracted and saved to {output_file}")
            else:
                messagebox.showerror("File Error", "Output file not found after extraction.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Execution Error", f"Failed to extract hidden text.\nError: {e.stderr}")

    def read_hidden_text(self):
        jpg_file = self.image_entry.get()
        output_file = os.path.splitext(jpg_file)[0] + ".txt"

        if os.path.exists(output_file):
            with open(output_file, 'r') as file:
                hidden_text = file.read()
            self.text_box.delete(1.0, tk.END)  # Clear the text box
            self.text_box.insert(tk.END, hidden_text)  # Insert the hidden text
        else:
            messagebox.showerror("File Error", "Output file does not exist. Please extract text first.")

    def check_install_stegosuite(self):
        try:
            subprocess.run("command -v stegosuite", shell=True, check=True, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError:
            install_choice = messagebox.askyesno("Install Stegosuite", "Stegosuite is not installed. Would you like to install it now?")
            if install_choice:
                self.install_stegosuite()

    def install_stegosuite(self):
        try:
            subprocess.run("sudo apt update && sudo apt install stegosuite -y", shell=True, check=True)
            messagebox.showinfo("Install Success", "Stegosuite installed successfully.")
        except subprocess.CalledProcessError:
            messagebox.showerror("Install Error", "Failed to install Stegosuite.")

if __name__ == "__main__":
    root = tk.Tk()
    gui = StegoSuiteGUI(root)
    root.mainloop()
