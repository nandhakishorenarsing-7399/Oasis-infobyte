import tkinter as tk
from tkinter import messagebox
import sqlite3
import datetime
import matplotlib.pyplot as plt

# ---------------- DATABASE SETUP ----------------
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

# ---------------- BMI FUNCTION ----------------
def calculate_bmi():
    try:
        name = name_entry.get()
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if weight <= 0 or height <= 0:
            raise ValueError

        bmi = weight / (height ** 2)
        bmi = round(bmi, 2)

        result_label.config(text=f"BMI: {bmi}")

        category = ""
        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 24.9:
            category = "Normal"
        elif bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obese"

        category_label.config(text=f"Category: {category}")

        # Save to DB
        cursor.execute("INSERT INTO users (name, weight, height, bmi, date) VALUES (?, ?, ?, ?, ?)",
                       (name, weight, height, bmi, datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        conn.commit()

    except ValueError:
        messagebox.showerror("Error", "Enter valid positive numbers!")

# ---------------- VIEW HISTORY ----------------
def view_history():
    name = name_entry.get()

    cursor.execute("SELECT date, bmi FROM users WHERE name=?", (name,))
    records = cursor.fetchall()

    if not records:
        messagebox.showinfo("Info", "No data found!")
        return

    history_window = tk.Toplevel(root)
    history_window.title("BMI History")

    for i, record in enumerate(records):
        tk.Label(history_window, text=f"{record[0]} → BMI: {record[1]}").pack()

# ---------------- GRAPH ----------------
def show_graph():
    name = name_entry.get()

    cursor.execute("SELECT date, bmi FROM users WHERE name=?", (name,))
    records = cursor.fetchall()

    if not records:
        messagebox.showinfo("Info", "No data to plot!")
        return

    dates = [r[0] for r in records]
    bmis = [r[1] for r in records]

    plt.figure()
    plt.plot(dates, bmis, marker='o')
    plt.xticks(rotation=45)
    plt.title(f"BMI Trend for {name}")
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.tight_layout()
    plt.show()

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Advanced BMI Calculator")
root.geometry("400x400")

tk.Label(root, text="BMI Calculator", font=("Arial", 16)).pack(pady=10)

# Name
tk.Label(root, text="Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()

# Weight
tk.Label(root, text="Weight (kg)").pack()
weight_entry = tk.Entry(root)
weight_entry.pack()

# Height
tk.Label(root, text="Height (m)").pack()
height_entry = tk.Entry(root)
height_entry.pack()

# Buttons
tk.Button(root, text="Calculate BMI", command=calculate_bmi).pack(pady=10)
tk.Button(root, text="View History", command=view_history).pack()
tk.Button(root, text="Show Graph", command=show_graph).pack(pady=5)

# Results
result_label = tk.Label(root, text="")
result_label.pack(pady=10)

category_label = tk.Label(root, text="")
category_label.pack()

root.mainloop()