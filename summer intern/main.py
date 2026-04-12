import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import datetime
import random
import math

# ---------------- DATABASE ----------------
conn = sqlite3.connect("bmi_marvel.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    bmi REAL,
    character TEXT,
    date TEXT
)
""")
conn.commit()

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("⚡ Marvel BMI Analyzer")
root.geometry("500x650")
root.resizable(False, False)

canvas = tk.Canvas(root, width=500, height=650, highlightthickness=0)
canvas.pack(fill="both", expand=True)

# ---------------- ANIMATED GRADIENT ----------------
gradient_colors = [
    (15, 32, 39),
    (44, 83, 100),
    (32, 58, 67),
    (20, 20, 20)
]

offset = 0

def draw_gradient():
    global offset
    canvas.delete("gradient")

    for i in range(0, 650, 5):
        r = int(20 + 20 * math.sin(i/50 + offset))
        g = int(80 + 40 * math.sin(i/60 + offset))
        b = int(120 + 60 * math.sin(i/70 + offset))

        color = f"#{r:02x}{g:02x}{b:02x}"
        canvas.create_line(0, i, 500, i, fill=color, tags="gradient")

    offset += 0.05
    root.after(50, draw_gradient)

# ---------------- PARTICLES ----------------
particles = []

for _ in range(40):
    particles.append({
        "x": random.randint(0, 500),
        "y": random.randint(0, 650),
        "size": random.randint(2, 4),
        "speed": random.uniform(0.5, 1.5)
    })

def animate_particles():
    canvas.delete("particles")

    for p in particles:
        p["y"] -= p["speed"]
        if p["y"] < 0:
            p["y"] = 650
            p["x"] = random.randint(0, 500)

        canvas.create_oval(
            p["x"], p["y"],
            p["x"] + p["size"], p["y"] + p["size"],
            fill="white", outline="", tags="particles"
        )

    root.after(50, animate_particles)

# ---------------- UI FRAME ----------------
frame = tk.Frame(root, bg="#111", bd=0)
frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=500)

title = tk.Label(frame, text="🦸 Marvel BMI Analyzer",
                 font=("Arial", 16, "bold"), fg="cyan", bg="#111")
title.pack(pady=10)

# Inputs
tk.Label(frame, text="Name", fg="white", bg="#111").pack()
name_entry = tk.Entry(frame)
name_entry.pack()

tk.Label(frame, text="Weight (kg)", fg="white", bg="#111").pack()
weight_entry = tk.Entry(frame)
weight_entry.pack()

tk.Label(frame, text="Height (m)", fg="white", bg="#111").pack()
height_entry = tk.Entry(frame)
height_entry.pack()

# Output labels
result_label = tk.Label(frame, text="", font=("Arial", 18, "bold"), fg="white", bg="#111")
result_label.pack(pady=10)

char_label = tk.Label(frame, text="", font=("Arial", 14, "bold"), fg="yellow", bg="#111")
char_label.pack()

image_label = tk.Label(frame, bg="#111")
image_label.pack(pady=10)

# ---------------- GLOW ANIMATION ----------------
def glow_text(color):
    def pulse(val):
        glow = int(100 + 155 * abs(math.sin(val)))
        hex_color = f"#{glow:02x}{glow:02x}{glow:02x}"
        result_label.config(fg=hex_color)
        root.after(50, pulse, val + 0.1)

    pulse(0)

# ---------------- IMAGE ----------------
def load_image(path):
    try:
        img = Image.open(path)
        img = img.resize((150, 150))
        photo = ImageTk.PhotoImage(img)

        image_label.config(image=photo)
        image_label.image = photo
    except:
        image_label.config(text="No Image", fg="white")

# ---------------- BMI LOGIC ----------------
def calculate_bmi():
    try:
        name = name_entry.get()
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        bmi = round(weight / (height ** 2), 2)

        if bmi < 18.5:
            char = "Spider-Man"
            img = "images/spiderman.png"
            color = "#ff3b3b"
        elif bmi < 24.9:
            char = "Captain America"
            img = "images/captain.png"
            color = "#3b82f6"
        elif bmi < 29.9:
            char = "Thor"
            img = "images/thor.png"
            color = "#9ca3af"
        else:
            char = "Hulk"
            img = "images/hulk.png"
            color = "#22c55e"

        result_label.config(text=f"BMI: {bmi}")
        char_label.config(text=f"You are: {char}")

        glow_text(color)
        load_image(img)

        cursor.execute("INSERT INTO records (name, bmi, character, date) VALUES (?, ?, ?, ?)",
                       (name, bmi, char, datetime.datetime.now()))
        conn.commit()

    except:
        messagebox.showerror("Error", "Invalid input!")

# Button
tk.Button(frame, text="Reveal My Hero ⚡",
          command=calculate_bmi,
          bg="#e11d48", fg="white",
          font=("Arial", 12, "bold")).pack(pady=15)

# ---------------- START ANIMATION ----------------
draw_gradient()
animate_particles()

root.mainloop()