#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog, messagebox, Text, Button, Scale, LEFT, RIGHT, Frame, Label
from PIL import Image, ImageTk
import subprocess
import os

class StegXApp:
    def __init__(self, master):
        self.master = master
        master.title("StegX")
        master.geometry("800x400")
        master.configure(bg="#2E2E2E")

        # Create left frame for file selection and password entry
        self.left_frame = Frame(master, bg="#2E2E2E")
        self.left_frame.pack(side=LEFT, padx=10, pady=10)

        # Select JPG File Button
        self.select_button = Button(self.left_frame, text="Select JPG File", command=self.select_file, bg="#4B4B4B", fg="white")
        self.select_button.pack(pady=5)

        # Thumbnail Display
        self.thumbnail_label = Label(self.left_frame, bg="#2E2E2E")
        self.thumbnail_label.pack(pady=5)

        # Password Entry
        self.password_label = Label(self.left_frame, text="Enter Password:", bg="#2E2E2E", fg="white")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.left_frame, show='*')
        self.password_entry.pack(pady=5)

        # Center Extract Button
        self.extract_button = Button(master, text="Extract Text", command=self.extract_text, bg="#4B4B4B", fg="white")
        self.extract_button.pack(pady=10)

        # Right Frame for Text Display
        self.right_frame = Frame(master, bg="#2E2E2E")
        self.right_frame.pack(side=RIGHT, padx=10, pady=10)

        # Text Display Area
        self.text_display = Text(self.right_frame, width=40, height=20, wrap='word', bg="#3E3E3E", fg="white", font=("Courier", 10))
        self.text_display.pack(pady=5)

        # Save Button
        self.save_button = Button(self.right_frame, text="Save Extracted Text", command=self.save_text, bg="#4B4B4B", fg="white")
        self.save_button.pack(pady=5)

        # Reset Button
        self.reset_button = Button(master, text="Reset", command=self.reset, bg="#4B4B4B", fg="white")
        self.reset_button.pack(pady=10)

        # Font Size Adjustment
        self.font_size_scale = Scale(master, from_=8, to=32, orient="horizontal", label="Font Size", command=self.change_font_size, bg="#2E2E2E")
        self.font_size_scale.set(10)
        self.font_size_scale.pack(pady=10)

        self.file_path = None

    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg")])
        if self.file_path:
            self.display_thumbnail()
    
    def display_thumbnail(self):
        # Clear previous thumbnail
        self.thumbnail_label.config(image='')
        image = Image.open(self.file_path)
        image.thumbnail((150, 150))  # Create thumbnail
        self.thumbnail_image = ImageTk.PhotoImage(image)
        self.thumbnail_label.config(image=self.thumbnail_image)

    def extract_text(self):
        if not self.file_path:
            messagebox.showerror("Error", "No file selected.")
            return
        
        password = self.password_entry.get()
        output_file = f"{os.path.splitext(self.file_path)[0]}.txt"
        
        try:
            result = subprocess.run(['stegosuite', 'extract', '-k', password, self.file_path], capture_output=True, text=True)
            if result.returncode == 0:
                with open(output_file, 'r') as f:
                    extracted_text = f.read()
                self.text_display.delete(1.0, tk.END)  # Clear previous text
                self.text_display.insert(tk.END, extracted_text)
            else:
                messagebox.showerror("Error", f"Failed to extract hidden text: {result.stderr.strip()}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def save_text(self):
        extracted_text = self.text_display.get(1.0, tk.END).strip()
        if not extracted_text:
            messagebox.showwarning("Warning", "No text to save.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if save_path:
            with open(save_path, 'w') as f:
                f.write(extracted_text)
            messagebox.showinfo("Success", "Text saved successfully.")

    def reset(self):
        self.file_path = None
        self.thumbnail_label.config(image='')
        self.text_display.delete(1.0, tk.END)
        self.password_entry.delete(0, tk.END)

    def change_font_size(self, size):
        self.text_display.config(font=("Courier", int(size)))

if __name__ == "__main__":
    root = tk.Tk()
    app = StegXApp(root)
    root.mainloop()
