#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import os
import subprocess

class StegXApp:
    def __init__(self, master):
        self.master = master
        self.master.title("StegX")
        self.master.configure(bg='darkgray')

        # Left Frame
        self.left_frame = tk.Frame(self.master, bg='darkgray')
        self.left_frame.grid(row=0, column=0, padx=10, pady=10)

        # Select JPG File
        self.select_button = tk.Button(self.left_frame, text="Select JPG File", command=self.select_file)
        self.select_button.grid(row=0, column=0, pady=5)

        self.thumbnail_label = tk.Label(self.left_frame, bg='darkgray')
        self.thumbnail_label.grid(row=1, column=0, pady=5)

        self.password_label = tk.Label(self.left_frame, text="Enter Password:", bg='darkgray')
        self.password_label.grid(row=2, column=0, pady=5)

        self.password_entry = tk.Entry(self.left_frame, show='*', bg='lightgray')
        self.password_entry.grid(row=3, column=0, pady=5)

        # Center Frame
        self.center_frame = tk.Frame(self.master, bg='darkgray')
        self.center_frame.grid(row=0, column=1, padx=10, pady=10)

        self.extract_button = tk.Button(self.center_frame, text="Extract Text", command=self.extract_text)
        self.extract_button.grid(row=0, column=0, pady=5)

        self.reset_button = tk.Button(self.center_frame, text="Reset", command=self.reset)
        self.reset_button.grid(row=1, column=0, pady=5)

        # Right Frame
        self.right_frame = tk.Frame(self.master, bg='darkgray')
        self.right_frame.grid(row=0, column=2, padx=10, pady=10)

        self.text_box = scrolledtext.ScrolledText(self.right_frame, width=40, height=20, wrap=tk.WORD, bg='lightgray', font=("Arial", 12))
        self.text_box.grid(row=0, column=0, pady=5)

        self.save_button = tk.Button(self.right_frame, text="Save Extracted Text", command=self.save_text)
        self.save_button.grid(row=1, column=0, pady=5)

        # Font Size Scale
        self.font_size_scale = tk.Scale(self.right_frame, from_=8, to=24, orient=tk.HORIZONTAL, label="Font Size", bg='darkgray', command=self.change_font_size)
        self.font_size_scale.set(12)  # Default font size
        self.font_size_scale.grid(row=2, column=0, pady=5)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg;*.jpeg")])
        if file_path:
            self.display_thumbnail(file_path)
            self.selected_file = file_path  # Store the selected file path

    def display_thumbnail(self, file_path):
        image = Image.open(file_path)
        image.thumbnail((100, 100))  # Resize for thumbnail
        self.thumbnail_image = ImageTk.PhotoImage(image)
        self.thumbnail_label.configure(image=self.thumbnail_image)
        self.thumbnail_label.image = self.thumbnail_image  # Keep a reference

    def extract_text(self):
        if not hasattr(self, 'selected_file'):
            messagebox.showerror("Error", "Please select a JPG file first.")
            return

        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Please enter a password.")
            return

        output_file = self.selected_file.rsplit('.', 1)[0] + "_extracted.txt"
        
        # Running the extraction command
        try:
            result = subprocess.run(['stegosuite', 'extract', '-k', password, self.selected_file], capture_output=True, text=True)
            if result.returncode == 0:
                with open(output_file, 'w') as f:
                    f.write(result.stdout)
                self.text_box.delete(1.0, tk.END)
                self.text_box.insert(tk.END, result.stdout)
                messagebox.showinfo("Success", f"Hidden text extracted and saved to {output_file}")
            else:
                messagebox.showerror("Error", f"Failed to extract hidden text: {result.stderr}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_text(self):
        if not self.text_box.get(1.0, tk.END).strip():
            messagebox.showerror("Error", "No text to save.")
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if output_path:
            with open(output_path, 'w') as f:
                f.write(self.text_box.get(1.0, tk.END))

    def change_font_size(self, size):
        new_size = int(size)
        self.text_box.config(font=("Arial", new_size))

    def reset(self):
        self.thumbnail_label.configure(image='')
        self.text_box.delete(1.0, tk.END)
        self.password_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = StegXApp(root)
    root.mainloop()
