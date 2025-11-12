
---

### 🧱 `expense_tracker.py`

```python
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from tabulate import tabulate

# Database setup
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    amount REAL NOT NULL,
                    date TEXT NOT NULL
                )''')
conn.commit()

def add_expense():
    category = input("Enter category (e.g., Food, Travel, Bills): ").title()
    amount = float(input("Enter amount: ₹"))
    date = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)", 
                   (category, amount, date))
    conn.commit()
    print("✅ Expense added successfully!")

def view_expenses():
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    if rows:
        print(tabulate(rows, headers=["ID", "Category", "Amount (₹)", "Date"], tablefmt="fancy_grid"))
    else:
        print("No expenses recorded yet.")

def summary_by_category():
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = cursor.fetchall()
    if data:
        print(tabulate(data, headers=["Category", "Total Spent (₹)"], tablefmt="grid"))
        categories = [x[0] for x in data]
        amounts = [x[1] for x in data]
        plt.pie(amounts, labels=categories, autopct="%1.1f%%")
        plt.title("Expense Distribution by Category")
        plt.show()
    else:
        print("No data to summarize.")

def monthly_summary():
    cursor.execute("SELECT strftime('%Y-%m', date) AS month, SUM(amount) FROM expenses GROUP BY month")
    data = cursor.fetchall()
    if data:
        months = [x[0] for x in data]
        amounts = [x[1] for x in data]
        plt.bar(months, amounts)
        plt.xlabel("Month")
        plt.ylabel("Total Spent (₹)")
        plt.title("Monthly Expense Summary")
        plt.show()
    else:
        print("No monthly data available.")

def main():
    while True:
        print("\n===== Personal Expense Tracker =====")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Category-wise Summary")
        print("4. Monthly Summary")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            summary_by_category()
        elif choice == "4":
            monthly_summary()
        elif choice == "5":
            print("💸 Exiting... Have a great day managing your expenses!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
