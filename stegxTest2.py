#!/usr/bin/env python3

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import subprocess

class StegXApp:
    def __init__(self, master):
        self.master = master
        self.master.title("StegX")
        self.master.configure(bg='black')

        # Frames for layout
        self.left_frame = tk.Frame(self.master, bg='black', width=450)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.middle_frame = tk.Frame(self.master, bg='black', width=100)
        self.middle_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.right_frame = tk.Frame(self.master, bg='black', width=450)
        self.right_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Widgets for left frame
        self.select_button = tk.Button(self.left_frame, text="Select File", command=self.select_file, bg='gray', fg='white')
        self.select_button.pack(pady=10)

        self.thumbnail_label = tk.Label(self.left_frame, bg='black')
        self.thumbnail_label.pack(pady=10)

        self.password_label = tk.Label(self.left_frame, text="Password:", bg='black', fg='white')
        self.password_label.pack(pady=5)

        self.password_entry = tk.Entry(self.left_frame, show='*')
        self.password_entry.pack(pady=5)

        # Widgets for middle frame
        self.extract_button = tk.Button(self.middle_frame, text="Extract", command=self.extract_text, bg='gray', fg='white')
        self.extract_button.pack(pady=10)

        self.reset_button = tk.Button(self.middle_frame, text="Reset", command=self.reset, bg='gray', fg='white')
        self.reset_button.pack(pady=10)

        self.font_size_label = tk.Label(self.middle_frame, text="Font Size:", bg='black', fg='white')
        self.font_size_label.pack(pady=5)

        self.font_size_scale = tk.Scale(self.middle_frame, from_=8, to=30, orient=tk.HORIZONTAL)
        self.font_size_scale.pack(pady=5)

        # Widgets for right frame
        self.text_display = tk.Text(self.right_frame, wrap=tk.WORD, bg='gray', fg='white', font=('Arial', 12))
        self.text_display.pack(expand=True, fill=tk.BOTH, pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg"), ("Audio files", "*.mp3;*.wav")])
        if file_path:
            self.display_thumbnail(file_path)
            self.selected_file = file_path

    def display_thumbnail(self, file_path):
        if file_path.lower().endswith(('.jpg', '.jpeg')):
            img = Image.open(file_path)
            img.thumbnail((300, 300))
            self.thumbnail = ImageTk.PhotoImage(img)
            self.thumbnail_label.config(image=self.thumbnail)
        else:
            self.thumbnail_label.config(image='')

    def extract_text(self):
        if not hasattr(self, 'selected_file'):
            messagebox.showerror("Error", "Please select a file first.")
            return

        password = self.password_entry.get()
        output_file = f"{os.path.splitext(self.selected_file)[0]}.txt"

        # Use Stegosuite for extraction
        process = subprocess.run(['stegosuite', 'extract', '-k', password, self.selected_file], capture_output=True, text=True)

        if process.returncode == 0:
            with open(output_file, 'w') as f:
                f.write(process.stdout)
            self.display_extracted_text(output_file)
            messagebox.showinfo("Success", f"Hidden text extracted to {output_file}")
        else:
            messagebox.showerror("Error", f"Failed to extract text: {process.stderr}")

    def display_extracted_text(self, output_file):
        with open(output_file, 'r') as f:
            self.text_display.delete(1.0, tk.END)  # Clear existing text
            self.text_display.insert(tk.END, f.read())  # Insert new text

    def reset(self):
        self.thumbnail_label.config(image='')
        self.password_entry.delete(0, tk.END)
        self.text_display.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = StegXApp(root)
    root.mainloop()
