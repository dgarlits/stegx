#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from PIL import Image, ImageTk
from stegano import lsb

class StegXApp:
    def __init__(self, master):
        self.master = master
        self.master.title("StegX")
        self.master.configure(bg='black')

        # Configure grid layout
        self.master.grid_columnconfigure(0, weight=45)  # Left column
        self.master.grid_columnconfigure(1, weight=10)  # Center column
        self.master.grid_columnconfigure(2, weight=45)  # Right column

        # Left frame for file selection, thumbnail, and password
        self.left_frame = tk.Frame(self.master, bg='black')
        self.left_frame.grid(row=0, column=0, sticky='nsew')

        # Select JPG file button
        self.file_button = tk.Button(self.left_frame, text="Select JPG File", command=self.select_file, fg='white', bg='gray')
        self.file_button.pack(pady=10)

        # Thumbnail display
        self.thumbnail_label = tk.Label(self.left_frame, bg='black')
        self.thumbnail_label.pack(pady=10)

        # Password input
        self.password_label = tk.Label(self.left_frame, text="Enter Password:", bg='black', fg='white')
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.left_frame, show='*', bg='gray', fg='white')
        self.password_entry.pack(pady=5)

        # Center frame for buttons
        self.center_frame = tk.Frame(self.master, bg='black')
        self.center_frame.grid(row=0, column=1, sticky='nsew')

        # Extract and reset buttons
        self.extract_button = tk.Button(self.center_frame, text="Extract Text", command=self.extract_text, fg='white', bg='gray')
        self.extract_button.pack(pady=10)

        self.reset_button = tk.Button(self.center_frame, text="Reset", command=self.reset, fg='white', bg='gray')
        self.reset_button.pack(pady=10)

        # Right frame for text display
        self.right_frame = tk.Frame(self.master, bg='black')
        self.right_frame.grid(row=0, column=2, sticky='nsew')

        # Text display box (should fill the right frame)
        self.text_display = scrolledtext.ScrolledText(self.right_frame, bg='gray', fg='white', wrap=tk.WORD)
        self.text_display.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Save extracted text button
        self.save_button = tk.Button(self.right_frame, text="Save Extracted Text", command=self.save_text, fg='white', bg='gray')
        self.save_button.pack(pady=5)

        # Font size adjustment
        self.font_size_scale = tk.Scale(self.right_frame, from_=8, to=32, orient=tk.HORIZONTAL, label="Font Size", command=self.adjust_font_size, bg='black', fg='white')
        self.font_size_scale.set(12)  # Set default font size
        self.font_size_scale.pack(pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg;*.jpeg;*.JPG")])
        if file_path:
            self.show_thumbnail(file_path)

    def show_thumbnail(self, file_path):
        img = Image.open(file_path)
        img.thumbnail((300, 300))  # Resize thumbnail
        self.thumbnail = ImageTk.PhotoImage(img)
        self.thumbnail_label.config(image=self.thumbnail)

    def extract_text(self):
        file_path = self.file_button.cget("text")  # Get the file path from button text
        password = self.password_entry.get()
        if not file_path or not password:
            messagebox.showerror("Error", "Please select a file and enter a password.")
            return
        try:
            # Extract the text
            extracted_text = lsb.reveal(file_path, password=password)
            self.text_display.delete(1.0, tk.END)
            self.text_display.insert(tk.END, extracted_text)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract text: {str(e)}")

    def save_text(self):
        extracted_text = self.text_display.get(1.0, tk.END).strip()
        if not extracted_text:
            messagebox.showwarning("Warning", "No text to save.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(extracted_text)

    def reset(self):
        self.thumbnail_label.config(image='')
        self.password_entry.delete(0, tk.END)
        self.text_display.delete(1.0, tk.END)

    def adjust_font_size(self, size):
        self.text_display.config(font=("TkDefaultFont", int(size)))

if __name__ == "__main__":
    root = tk.Tk()
    app = StegXApp(root)
    root.mainloop()
