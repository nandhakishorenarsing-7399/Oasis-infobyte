import tkinter as tk
from tkinter import messagebox
import random
import string

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("450x400")
        
        # Password Length Label and Entry
        tk.Label(root, text="Password Length:", font=("Arial", 12)).pack(pady=10)
        self.length_entry = tk.Entry(root, font=("Arial", 12), width=20)
        self.length_entry.pack(pady=5)
        self.length_entry.insert(0, "12")
        
        # Checkboxes for character types
        tk.Label(root, text="Include:", font=("Arial", 12)).pack(pady=10)
        
        self.uppercase_var = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Uppercase Letters (A-Z)", variable=self.uppercase_var).pack()
        
        self.lowercase_var = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Lowercase Letters (a-z)", variable=self.lowercase_var).pack()
        
        self.digits_var = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Digits (0-9)", variable=self.digits_var).pack()
        
        self.special_var = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Special Characters (!@#$%)", variable=self.special_var).pack()
        
        # Generate Button
        tk.Button(root, text="Generate Password", command=self.generate_password, 
                  font=("Arial", 12), bg="blue", fg="white").pack(pady=20)
        
        # Password Display
        tk.Label(root, text="Generated Password:", font=("Arial", 12)).pack(pady=10)
        self.password_text = tk.Text(root, font=("Arial", 12), height=2, width=40)
        self.password_text.pack(pady=5)
        
        # Copy Button
        tk.Button(root, text="Copy to Clipboard", command=self.copy_password, 
                  font=("Arial", 10), bg="green", fg="white").pack(pady=5)
    
    def generate_password(self):
        try:
            length = int(self.length_entry.get())
            
            if length < 4:
                messagebox.showerror("Error", "Password length must be at least 4")
                return
            
            # Build character pool
            char_pool = ""
            if self.uppercase_var.get():
                char_pool += string.ascii_uppercase
            if self.lowercase_var.get():
                char_pool += string.ascii_lowercase
            if self.digits_var.get():
                char_pool += string.digits
            if self.special_var.get():
                char_pool += "!@#$%^&*"
            
            if not char_pool:
                messagebox.showerror("Error", "Select at least one character type")
                return
            
            # Generate password
            password = ''.join(random.choice(char_pool) for _ in range(length))
            
            self.password_text.delete(1.0, tk.END)
            self.password_text.insert(1.0, password)
        
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for password length")
    
    def copy_password(self):
        password = self.password_text.get(1.0, tk.END).strip()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showerror("Error", "No password to copy. Generate one first!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()
