import csv
import os
import tkinter as tk
from tkinter import simpledialog, messagebox
import matplotlib.pyplot as plt

class ExpenseTracker:
    def __init__(self, filename):
        self.filename = filename
        self.balance = 0
        self.expenses = {}
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.filename):
            return
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            if rows:
                self.balance = float(rows[0][0])
                for row in rows[1:]:
                    category, amount = row
                    self.expenses[category] = self.expenses.get(category, 0) + float(amount)

    def save_data(self):
        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.balance])
            for category, amount in self.expenses.items():
                writer.writerow([category, amount])

    def add_expense(self, amount, category):
        if amount > self.balance:
            messagebox.showerror("Error", "Not enough balance!")
            return
        self.balance -= amount
        self.expenses[category] = self.expenses.get(category, 0) + amount
        self.save_data()

    def add_income(self, amount):
        self.balance += amount
        self.save_data()

    def plot_expenses(self):
        if not self.expenses:
            messagebox.showinfo("Info", "No expenses to plot.")
            return
        categories = list(self.expenses.keys())
        amounts = list(self.expenses.values())

        plt.figure(figsize=(8, 6))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
        plt.title('Expense Distribution')
        plt.axis('equal')
        plt.show()

class ExpenseApp(tk.Tk):
    def __init__(self, tracker):
        super().__init__()
        self.tracker = tracker
        self.title("Expense Tracker")
        self.geometry("400x400")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Expense Tracker", font=("Arial", 20)).pack(pady=10)

        tk.Button(self, text="Add Expense", command=self.add_expense).pack(pady=5)
        tk.Button(self, text="Add Income", command=self.add_income).pack(pady=5)
        tk.Button(self, text="Show Balance", command=self.show_balance).pack(pady=5)
        tk.Button(self, text="Show Expenses", command=self.show_expenses).pack(pady=5)
        tk.Button(self, text="Show Expenses Graph", command=self.show_graph).pack(pady=5)
        tk.Button(self, text="Exit", command=self.destroy).pack(pady=20)

    def add_expense(self):
        amount = simpledialog.askfloat("Add Expense", "Enter expense amount:")
        if amount is None:
            return
        category = simpledialog.askstring("Add Expense", "Enter category:")
        if category:
            self.tracker.add_expense(amount, category)
            messagebox.showinfo("Success", f"Added ₹{amount} under '{category}'.")

    def add_income(self):
        amount = simpledialog.askfloat("Add Income", "Enter income amount:")
        if amount is None:
            return
        self.tracker.add_income(amount)
        messagebox.showinfo("Success", f"Added ₹{amount} to balance.")

    def show_balance(self):
        messagebox.showinfo("Current Balance", f"Your balance is ₹{self.tracker.balance}")

    def show_expenses(self):
        if not self.tracker.expenses:
            messagebox.showinfo("Expenses", "No expenses recorded yet.")
            return
        expense_text = "\n".join(f"{cat}: ₹{amt}" for cat, amt in self.tracker.expenses.items())
        messagebox.showinfo("Expenses", expense_text)

    def show_graph(self):
        self.tracker.plot_expenses()

def main():
    filename = "expenses.csv"
    tracker = ExpenseTracker(filename)
    app = ExpenseApp(tracker)
    app.mainloop()

if __name__ == "__main__":
    main()
