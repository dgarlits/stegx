#!/usr/bin/env python3

import os
import subprocess
from tkinter import filedialog, messagebox, Tk, Label, Button, Entry, PhotoImage, Frame, Canvas, Scrollbar
from tkinter.constants import BOTH, VERTICAL, HORIZONTAL

# Function to check if Stegosuite is installed
def check_stegosuite_installed():
    try:
        subprocess.run(["stegosuite", "--help"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        messagebox.showerror("Error", "Stegosuite is not installed. Please install it first.")
        return False
    return True

# Function to select JPG file
def select_jpg():
    jpgfile = filedialog.askopenfilename(title="Select JPG File", filetypes=[("JPG Files", "*.jpg")])
    if jpgfile:
        show_image(jpgfile)
    return jpgfile

# Function to show the selected image in a resizable window
def show_image(jpgfile):
    img = PhotoImage(file=jpgfile)
    canvas.create_image(0, 0, anchor="nw", image=img)
    canvas.image = img
    canvas.config(scrollregion=canvas.bbox("all"))
    root.update_idletasks()

# Function to save extracted text
def save_extracted_text(default_name):
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=default_name)
    return save_path

# Function to extract hidden text from the selected JPG
def extract_text():
    if not check_stegosuite_installed():
        return
    
    # Select JPG file
    jpgfile = select_jpg()
    if not jpgfile:
        messagebox.showerror("Error", "No file selected.")
        return

    # Get password from user
    password = password_entry.get()
    if not password:
        messagebox.showerror("Error", "Password is required.")
        return

    # Define default output file name
    default_output_file = os.path.basename(jpgfile).replace(".jpg", ".txt")
    
    # Ask where to save the extracted text
    output_file = save_extracted_text(default_output_file)
    if not output_file:
        messagebox.showerror("Error", "No output location selected.")
        return
    
    try:
        # Run Stegosuite command to extract text
        result = subprocess.run(
            ["stegosuite", "extract", "-k", password, jpgfile],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        if result.returncode == 0:
            with open(output_file, "w") as f:
                f.write(result.stdout.decode())
            messagebox.showinfo("Success", f"Hidden text extracted and saved to {output_file}")
        else:
            error_msg = result.stderr.decode() or "Unknown error"
            messagebox.showerror("Error", f"Failed to extract hidden text: {error_msg}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Extraction failed: {e.stderr.decode()}")

# GUI setup with dark theme
def create_gui():
    global root, password_entry, canvas
    
    root = Tk()
    root.title("Stegosuite Extractor")
    root.configure(bg="#2e2e2e")  # Dark background
    root.geometry("800x600")  # Set the initial size of the window

    # Frame for file selector and password
    top_frame = Frame(root, bg="#2e2e2e")
    top_frame.pack(fill="x", pady=10, padx=10)

    # Create a label with dark theme
    Label(top_frame, text="Stegosuite Extractor", fg="#ffffff", bg="#2e2e2e", font=("Arial", 16)).pack(pady=10)

    # Input for password with dark theme
    Label(top_frame, text="Enter Password:", fg="#ffffff", bg="#2e2e2e").pack()
    password_entry = Entry(top_frame, show="*", bg="#3c3c3c", fg="#ffffff", insertbackground="white")
    password_entry.pack(pady=5)

    # Extract button with dark theme
    extract_button = Button(top_frame, text="Extract Text from JPG", command=extract_text, bg="#565656", fg="#ffffff")
    extract_button.pack(pady=10)

    # Scrollable canvas for displaying image
    canvas_frame = Frame(root, bg="#2e2e2e")
    canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)

    canvas = Canvas(canvas_frame, bg="#1e1e1e", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    # Scrollbars for the image canvas
    x_scroll = Scrollbar(canvas_frame, orient=HORIZONTAL, command=canvas.xview)
    x_scroll.pack(side="bottom", fill="x")
    y_scroll = Scrollbar(canvas_frame, orient=VERTICAL, command=canvas.yview)
    y_scroll.pack(side="right", fill="y")

    canvas.config(xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
