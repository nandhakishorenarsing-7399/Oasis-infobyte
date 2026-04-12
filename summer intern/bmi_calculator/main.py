import tkinter as tk
from tkinter import messagebox

class BMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")
        self.root.geometry("400x300")
        
        # Weight Label and Entry
        tk.Label(root, text="Weight (kg):", font=("Arial", 12)).pack(pady=5)
        self.weight_entry = tk.Entry(root, font=("Arial", 12), width=20)
        self.weight_entry.pack(pady=5)
        
        # Height Label and Entry
        tk.Label(root, text="Height (m):", font=("Arial", 12)).pack(pady=5)
        self.height_entry = tk.Entry(root, font=("Arial", 12), width=20)
        self.height_entry.pack(pady=5)
        
        # Calculate Button
        tk.Button(root, text="Calculate BMI", command=self.calculate_bmi, 
                  font=("Arial", 12), bg="green", fg="white").pack(pady=20)
        
        # Result Label
        self.result_label = tk.Label(root, text="", font=("Arial", 14), fg="blue")
        self.result_label.pack(pady=10)
    
    def calculate_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            
            if weight <= 0 or height <= 0:
                messagebox.showerror("Error", "Weight and height must be positive values")
                return
            
            bmi = weight / (height ** 2)
            self.result_label.config(text=f"BMI: {bmi:.2f}")
            
            # BMI Categories
            if bmi < 18.5:
                category = "Underweight"
            elif 18.5 <= bmi < 25:
                category = "Normal weight"
            elif 25 <= bmi < 30:
                category = "Overweight"
            else:
                category = "Obese"
            
            messagebox.showinfo("BMI Result", f"BMI: {bmi:.2f}\nCategory: {category}")
        
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values")

if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculator(root)
    root.mainloop()
