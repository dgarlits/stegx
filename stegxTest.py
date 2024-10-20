#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

class StegXApp:
    def __init__(self, master):
        self.master = master
        self.master.title("StegX - Stegosuite Frontend")
        self.master.configure(bg='black')
        
        # Check if Stegosuite is installed
        self.check_install_stegosuite()

        # Layout frames
        self.left_frame = tk.Frame(master, bg='black')
        self.middle_frame = tk.Frame(master, bg='black', width=100)
        self.right_frame = tk.Frame(master, bg='black')

        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.middle_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Left Frame Widgets
        self.file_label = tk.Label(self.left_frame, text="Select JPG/MP3/WAV File", bg='black', fg='white')
        self.file_label.pack(pady=5)

        self.file_button = tk.Button(self.left_frame, text="Browse", command=self.select_file, bg='gray', fg='white')
        self.file_button.pack(pady=5)

        self.password_label = tk.Label(self.left_frame, text="Password (if any)", bg='black', fg='white')
        self.password_label.pack(pady=5)

        self.password_entry = tk.Entry(self.left_frame, show='*', bg='gray', fg='white')
        self.password_entry.pack(pady=5)

        # Middle Frame Widgets
        self.extract_button = tk.Button(self.middle_frame, text="Extract Hidden Text", command=self.extract_text, bg='gray', fg='white')
        self.extract_button.pack(pady=5)

        self.reset_button = tk.Button(self.middle_frame, text="Reset", command=self.reset, bg='gray', fg='white')
        self.reset_button.pack(pady=5)

        # Right Frame Widgets
        self.text_display = tk.Text(self.right_frame, wrap=tk.WORD, bg='gray', fg='white', height=20)
        self.text_display.pack(fill=tk.BOTH, expand=True, pady=5)

        self.save_button = tk.Button(self.right_frame, text="Save Extracted Text", command=self.save_text, bg='gray', fg='white')
        self.save_button.pack(pady=5)

        self.quit_button = tk.Button(self.right_frame, text="Quit", command=self.master.quit, bg='gray', fg='white')
        self.quit_button.pack(pady=5)

    def check_install_stegosuite(self):
        try:
            result = subprocess.run(['command', '-v', 'stegosuite'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                raise FileNotFoundError("Stegosuite not found.")
        except FileNotFoundError:
            install = messagebox.askyesno("Stegosuite Not Found", "Stegosuite is not installed. Would you like to install it?")
            if install:
                self.install_stegosuite()
            else:
                self.master.quit()

    def install_stegosuite(self):
        try:
            subprocess.run(['sudo', 'apt', 'update'], check=True)
            subprocess.run(['sudo', 'apt', 'install', 'stegosuite', '-y'], check=True)
            messagebox.showinfo("Success", "Stegosuite installed successfully.")
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Failed to install Stegosuite. Exiting...")
            self.master.quit()

    def select_file(self):
        # Updated file types to include JPG, MP3, and WAV
        file_types = [("Image files", "*.jpg;*.jpeg"), 
                      ("Audio files", "*.mp3;*.wav"),
                      ("All files", "*.*")]
        self.file_path = filedialog.askopenfilename(filetypes=file_types)
        if self.file_path:
            messagebox.showinfo("Selected File", f"You selected: {os.path.basename(self.file_path)}")

    def extract_text(self):
        if hasattr(self, 'file_path'):
            password = self.password_entry.get()
            output_file = f"{os.path.splitext(self.file_path)[0]}.txt"

            try:
                # Call Stegosuite to extract the hidden text
                subprocess.run(['stegosuite', 'extract', '-k', password, self.file_path, '-o', output_file], check=True)
                with open(output_file, 'r') as file:
                    hidden_text = file.read()
                self.text_display.delete(1.0, tk.END)
                self.text_display.insert(tk.END, hidden_text)
                messagebox.showinfo("Success", f"Hidden text extracted to {output_file}")
            except subprocess.CalledProcessError:
                messagebox.showerror("Error", "Failed to extract hidden text. Please check the password or file.")
        else:
            messagebox.showwarning("Warning", "Please select a JPG/MP3/WAV file first.")

    def save_text(self):
        if self.text_display.get(1.0, tk.END).strip():
            save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if save_path:
                with open(save_path, 'w') as file:
                    file.write(self.text_display.get(1.0, tk.END))
        else:
            messagebox.showwarning("Warning", "No text to save.")

    def reset(self):
        self.text_display.delete(1.0, tk.END)
        self.password_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = StegXApp(root)
    root.mainloop()
