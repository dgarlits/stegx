def extract_text(self):
    if not self.selected_file:
        messagebox.showerror("Error", "Please select a file first.")
        return

    password = self.password_entry.get()  # Get the password from the entry field

    command = ['stegosuite', 'extract', '-k', password, self.selected_file]
    print(f"Running command: {' '.join(command)}")  # Print the command for debugging

    try:
        # Capture the output directly from the subprocess
        process = subprocess.run(command, capture_output=True, text=True)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run Stegosuite: {e}")
        return

    # Output process results for debugging
    print(f"STDOUT: {process.stdout}")
    print(f"STDERR: {process.stderr}")

    if process.returncode == 0:
        extracted_text = process.stdout.strip()  # Capture the text from stdout
        
        try:
            font_size = int(self.font_size_entry.get())
            if font_size < 12 or font_size > 22:
                raise ValueError("Font size must be between 12 and 22.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        # Display extracted text in the text display area
        self.text_display.config(font=('Arial', font_size), fg="white")
        self.text_display.delete(1.0, tk.END)  # Clear existing text
        self.text_display.insert(tk.END, extracted_text)  # Insert new text
    else:
        messagebox.showerror("Error",
