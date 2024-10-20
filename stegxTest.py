import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import io

class StegX:
    def __init__(self, master):
        self.master = master
        self.master.title("StegX")
        self.master.configure(bg='#2E2E2E')

        # Frame for the left side
        self.left_frame = tk.Frame(self.master, bg='#2E2E2E', padx=10, pady=10)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, expand=True)

        # File selector
        self.file_button = tk.Button(self.left_frame, text="Select JPG File", command=self.select_file, fg='white', bg='#4C4C4C')
        self.file_button.pack(pady=5)

        # Thumbnail Label
        self.thumbnail_label = tk.Label(self.left_frame, bg='#2E2E2E')
        self.thumbnail_label.pack(pady=5)

        # Password Entry
        self.password_label = tk.Label(self.left_frame, text="Password:", fg='white', bg='#2E2E2E')
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.left_frame, show='*')
        self.password_entry.pack(pady=5)

        # Center Frame for Buttons
        self.center_frame = tk.Frame(self.master, bg='#2E2E2E')
        self.center_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Extract Text Button
        self.extract_button = tk.Button(self.center_frame, text="Extract Text", command=self.extract_text, fg='white', bg='#4C4C4C')
        self.extract_button.pack(pady=20)

        # Reset Button
        self.reset_button = tk.Button(self.center_frame, text="Reset", command=self.reset, fg='white', bg='#4C4C4C')
        self.reset_button.pack(pady=5)

        # Right Frame for Text Display
        self.right_frame = tk.Frame(self.master, bg='#2E2E2E')
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Text Display Box
        self.text_display = tk.Text(self.right_frame, wrap='word', bg='#1E1E1E', fg='white', font=("TkDefaultFont", 12))
        self.text_display.pack(fill=tk.BOTH, expand=True)

        # Font Size Control
        self.font_size_scale = tk.Scale(self.right_frame, from_=8, to=24, orient='horizontal', label='Font Size', command=self.change_font_size)
        self.font_size_scale.set(12)  # Default font size
        self.font_size_scale.pack(pady=5)

        # Save Extracted Text Button
        self.save_button = tk.Button(self.right_frame, text="Save Extracted Text", command=self.save_extracted_text, fg='white', bg='#4C4C4C')
        self.save_button.pack(pady=5)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.*")])
        if file_path:
            self.load_thumbnail(file_path)

    def load_thumbnail(self, file_path):
        img = Image.open(file_path)
        # Resize thumbnail to fit within the available width while maintaining aspect ratio
        width = self.left_frame.winfo_width()
        img.thumbnail((width, width), Image.ANTIALIAS)
        self.img_tk = ImageTk.PhotoImage(img)
        self.thumbnail_label.configure(image=self.img_tk)
        self.thumbnail_label.image = self.img_tk  # Keep a reference to avoid garbage collection

    def extract_text(self):
        # Placeholder for extraction logic
        messagebox.showinfo("Extract", "Text extraction logic goes here.")

    def save_extracted_text(self):
        # Save logic placeholder
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                  filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'w') as f:
                f.write(self.text_display.get("1.0", tk.END))

    def change_font_size(self, size):
        self.text_display.config(font=("TkDefaultFont", size))

    def reset(self):
        self.thumbnail_label.configure(image=None)
        self.text_display.delete('1.0', tk.END)
        self.password_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = StegX(root)
    root.mainloop()
