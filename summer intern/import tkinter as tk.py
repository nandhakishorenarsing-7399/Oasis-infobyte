import tkinter as tk
from tkinter import messagebox
import string
import secrets
import math

# ---------------------------
# PASSWORD LOGIC
# ---------------------------

def generate_password():
    length = int(length_var.get())

    if length < 6:
        messagebox.showerror("Error", "Minimum 6 characters required")
        return

    exclude_chars = exclude_entry.get()

    upper = [c for c in string.ascii_uppercase if c not in exclude_chars]
    lower = [c for c in string.ascii_lowercase if c not in exclude_chars]
    digits = [c for c in string.digits if c not in exclude_chars]
    symbols = [c for c in string.punctuation if c not in exclude_chars]

    selected = []
    if upper_var.get(): selected.append(upper)
    if lower_var.get(): selected.append(lower)
    if digit_var.get(): selected.append(digits)
    if symbol_var.get(): selected.append(symbols)

    if not selected:
        messagebox.showerror("Error", "Select at least one option")
        return

    password = [secrets.choice(s) for s in selected]
    all_chars = [c for group in selected for c in group]

    password += [secrets.choice(all_chars) for _ in range(length - len(password))]
    secrets.SystemRandom().shuffle(password)

    pwd = ''.join(password)
    password_var.set(pwd)
    update_strength(pwd)


def update_strength(password):
    score = 0
    if len(password) >= 8: score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c.islower() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c in string.punctuation for c in password): score += 1

    if score <= 2:
        strength_label.config(text="Weak", fg="#ff4d4d")
    elif score <= 4:
        strength_label.config(text="Medium", fg="#ffaa00")
    else:
        strength_label.config(text="Strong", fg="#00ffcc")


def copy_password():
    pwd = password_var.get()
    if pwd:
        root.clipboard_clear()
        root.clipboard_append(pwd)
        root.update()
        messagebox.showinfo("Copied", "Password copied!")

# ---------------------------
# UI
# ---------------------------

root = tk.Tk()
root.title("Glass Password Generator")
root.geometry("600x600")
root.resizable(False, False)

canvas = tk.Canvas(root, width=600, height=600)
canvas.pack(fill="both", expand=True)

# ---------------------------
# ANIMATED GRADIENT BACKGROUND
# ---------------------------

angle = 0

def animate_bg():
    global angle
    canvas.delete("bg")

    for i in range(0, 600, 2):
        r = int(128 + 127 * math.sin((i + angle) * 0.01))
        g = int(128 + 127 * math.sin((i + angle) * 0.015))
        b = int(128 + 127 * math.sin((i + angle) * 0.02))
        color = f'#{r:02x}{g:02x}{b:02x}'
        canvas.create_line(0, i, 600, i, fill=color, tags="bg")

    angle += 5
    root.after(50, animate_bg)

animate_bg()

# ---------------------------
# GLASS PANEL
# ---------------------------

panel = tk.Frame(root, bg="#ffffff", bd=0)
panel.place(relx=0.5, rely=0.5, anchor="center", width=400, height=500)

panel.configure(bg="#ffffff")
panel.attributes = {"alpha": 0.85}  # pseudo glass feel

# ---------------------------
# VARIABLES
# ---------------------------

length_var = tk.IntVar(value=12)
upper_var = tk.BooleanVar(value=True)
lower_var = tk.BooleanVar(value=True)
digit_var = tk.BooleanVar(value=True)
symbol_var = tk.BooleanVar(value=True)
password_var = tk.StringVar()

# ---------------------------
# CONTENT
# ---------------------------

title = tk.Label(panel, text="🔐 Password Lab",
                 font=("Segoe UI", 16, "bold"),
                 bg="#ffffff")
title.pack(pady=10)

length_label = tk.Label(panel, text="Length: 12",
                        bg="#ffffff")
length_label.pack()

slider = tk.Scale(panel, from_=6, to=32,
                  orient="horizontal",
                  variable=length_var,
                  bg="#ffffff",
                  highlightthickness=0)

slider.pack()

def update_len(val):
    length_label.config(text=f"Length: {int(val)}")

slider.config(command=update_len)

# OPTIONS
tk.Checkbutton(panel, text="Uppercase", variable=upper_var, bg="#ffffff").pack(anchor="w", padx=20)
tk.Checkbutton(panel, text="Lowercase", variable=lower_var, bg="#ffffff").pack(anchor="w", padx=20)
tk.Checkbutton(panel, text="Digits", variable=digit_var, bg="#ffffff").pack(anchor="w", padx=20)
tk.Checkbutton(panel, text="Symbols", variable=symbol_var, bg="#ffffff").pack(anchor="w", padx=20)

# EXCLUDE
tk.Label(panel, text="Exclude Characters", bg="#ffffff").pack()
exclude_entry = tk.Entry(panel)
exclude_entry.pack(pady=5)

# GENERATE BUTTON
gen_btn = tk.Button(panel, text="Generate",
                    command=generate_password,
                    bg="#00ccff", fg="black",
                    activebackground="#00ffaa")
gen_btn.pack(pady=10)

# OUTPUT
output = tk.Entry(panel, textvariable=password_var,
                  font=("Consolas", 12), justify="center")
output.pack(pady=10)

# STRENGTH
strength_label = tk.Label(panel, text="Strength: -", bg="#ffffff")
strength_label.pack()

# COPY
copy_btn = tk.Button(panel, text="Copy",
                     command=copy_password,
                     bg="#00ffaa")
copy_btn.pack(pady=10)

root.mainloop()