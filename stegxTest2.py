#!/usr/bin/env python3

import os  # Importing os for file name handling
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class StegXApp:
    def __init__(self, master):
        self.master = master
        self.master.title("StegX")
        self.master.configure(bg='black')

        # Initialize selected file variable
        self.selected_file = tk.StringVar()

        # Frames for layout
        self.left_frame = tk.Frame(self.master, bg='black')
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0))

        self.middle_frame = tk.Frame(self.master, bg='black')
        self.middle_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        self.right_frame = tk.Frame(self.master, bg='black')
        self.right_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # Widgets for left frame
        self.select_button = tk.Button(self.left_frame, text="Select File", command=self.select_file, bg='gray', fg='white')
        self.select_button.pack(pady=(10, 5))

        self.thumbnail_label = tk.Label(self.left_frame, bg='black')
        self.thumbnail_label.pack(pady=(5, 5))

        self.password_label = tk.Label(self.left_frame, text="Password:", bg='black', fg='white')
        self.password_label.pack(pady=5)

        self.password_entry = tk.Entry(self.left_frame, show='*')
        self.password_entry.pack(pady=5)

        # Display file name label at the bottom of the left column
        self.file_name_label = tk.Label(self.left_frame, text="", bg='black', fg='white')
        self.file_name_label.pack(side=tk.BOTTOM, pady=(5, 10))

        # Widgets for middle frame
        self.extract_button = tk.Button(self.middle_frame, text="Extract", command=self.extract_text, bg='gray', fg='white')
        self.extract_button.pack(pady=10)

        self.reset_button = tk.Button(self.middle_frame, text="Reset", command=self.reset, bg='gray', fg='white')
        self.reset_button.pack(pady=10)

        self.font_size_label = tk.Label(self.middle_frame, text="Font Size (12-22):", bg='black', fg='white')
        self.font_size_label.pack(pady=5)

        self.font_size_entry = tk.Entry(self.middle_frame)
        self.font_size_entry.pack(pady=5)
        self.font_size_entry.insert(0, "12")  # Default font size

        # Widgets for right frame
        self.text_display = tk.Text(self.right_frame, wrap=tk.WORD, bg='dimgray', fg='white', font=('Arial', 12))
        self.text_display.pack(expand=True, fill=tk.BOTH, pady=10)

    def select_file(self):
        filetypes = [('JPEG Files', '*.jpg'), ('All Files', '*.*')]
        file_path = filedialog.askopenfilename(title="Select a file", filetypes=filetypes)
        if file_path:
            try:
                # Load and display image
                img = Image.open(file_path)
                img.thumbnail((300, 300))  # Resize image to fit GUI window
                img_tk = ImageTk.PhotoImage(img)
                self.thumbnail_label.config(image=img_tk)
                self.thumbnail_label.image = img_tk  # Keep a reference to prevent garbage collection
                self.selected_file.set(file_path)  # Update selected file path
                self.file_name_label.config(text=os.path.basename(file_path))  # Display the file name at the bottom
            except Exception as e:
                messagebox.showerror("Error", f"Unable to open image: {str(e)}")

    def extract_text(self):
        file_path = self.selected_file.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a file first.")
            return

        password = self.password_entry.get()
        # Example: Replace with actual extraction logic
        extracted_text = f"Extracted text from {file_path} with password {password}"

        # Get the font size from the entry
        try:
            font_size = int(self.font_size_entry.get())
            if font_size < 12 or font_size > 22:
                raise ValueError("Font size must be between 12 and 22.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        self.text_display.config(font=('Arial', font_size))  # Update the font size using user input
        self.text_display.delete(1.0, tk.END)  # Clear existing text
        self.text_display.insert(tk.END, extracted_text)  # Insert new text

    def reset(self):
        self.thumbnail_label.config(image='')
        self.password_entry.delete(0, tk.END)
        self.text_display.delete(1.0, tk.END)
        self.file_name_label.config(text="")  # Clear the file name display
        self.selected_file.set('')  # Clear the selected file path

if __name__ == "__main__":
    root = tk.Tk()
    app = StegXApp(root)
    root.mainloop()
