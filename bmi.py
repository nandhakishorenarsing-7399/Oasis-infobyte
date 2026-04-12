import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import datetime

# ---------------- DATABASE ----------------
conn = sqlite3.connect("bmi_data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    weight REAL,
    height REAL,
    bmi REAL,
    date TEXT
)
""")
conn.commit()

# ---------------- MAIN FUNCTION ----------------
def calculate_bmi():
    try:
        name = name_entry.get()
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if weight <= 0 or height <= 0:
            raise ValueError

        bmi = round(weight / (height ** 2), 2)

        # Category logic
        if bmi < 18.5:
            category = "Underweight"
            color = "#87CEFA"
            img_path = "images/underweight.png"
        elif bmi < 24.9:
            category = "Normal"
            color = "#90EE90"
            img_path = "images/normal.png"
        elif bmi < 29.9:
            category = "Overweight"
            color = "#FFD580"
            img_path = "images/overweight.png"
        else:
            category = "Obese"
            color = "#FF7F7F"
            img_path = "images/obese.png"

        # Update UI
        result_label.config(text=f"BMI: {bmi}")
        category_label.config(text=f"{category}")
        root.configure(bg=color)

        animate_result()

        # Load Image
        load_image(img_path)

        # Save data
        cursor.execute("INSERT INTO users (name, weight, height, bmi, date) VALUES (?, ?, ?, ?, ?)",
                       (name, weight, height, bmi, datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        conn.commit()

    except:
        messagebox.showerror("Error", "Enter valid inputs!")

# ---------------- ANIMATION ----------------
def animate_result():
    def flash(count):
        if count % 2 == 0:
            result_label.config(fg="black")
        else:
            result_label.config(fg="white")
        if count < 6:
            root.after(200, flash, count + 1)

    flash(0)

# ---------------- IMAGE LOADER ----------------
def load_image(path):
    try:
        img = Image.open(path)
        img = img.resize((120, 120))
        photo = ImageTk.PhotoImage(img)

        image_label.config(image=photo)
        image_label.image = photo
    except:
        image_label.config(text="No Image")

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Smart BMI Calculator")
root.geometry("400x500")
root.configure(bg="#f0f0f0")

tk.Label(root, text="BMI Calculator", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)

# Inputs
tk.Label(root, text="Name", bg="#f0f0f0").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Weight (kg)", bg="#f0f0f0").pack()
weight_entry = tk.Entry(root)
weight_entry.pack()

tk.Label(root, text="Height (m)", bg="#f0f0f0").pack()
height_entry = tk.Entry(root)
height_entry.pack()

# Button
tk.Button(root, text="Calculate", command=calculate_bmi, bg="#333", fg="white").pack(pady=10)

# Results
result_label = tk.Label(root, text="", font=("Arial", 14), bg="#f0f0f0")
result_label.pack()

category_label = tk.Label(root, text="", font=("Arial", 12, "bold"), bg="#f0f0f0")
category_label.pack()

# Image
image_label = tk.Label(root, bg="#f0f0f0")
image_label.pack(pady=10)

root.mainloop()