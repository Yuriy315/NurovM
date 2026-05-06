import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import json
import os
from datetime import datetime


class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.data_file = "data/expenses.json"
        self.expenses = self.load_data()

        # --- Интерфейс ---
        # Поля ввода
        tk.Label(root, text="Сумма:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_amount = tk.Entry(root, width=15)
        self.entry_amount.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Категория:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_category = tk.Entry(root, width=15)
        self.entry_category.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Дата (ГГГГ-ММ-ДД):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_date = tk.Entry(root, width=15)
        self.entry_date.grid(row=2, column=1, padx=5, pady=5)

        # Кнопка добавления расхода
        self.btn_add = tk.Button(root, text="Добавить расход", command=self.add_expense)
        self.btn_add.grid(row=3, column=0, columnspan=2, pady=10)

        # Таблица расходов
        self.tree = ttk.Treeview(root, columns=("amount", "category", "date"), show="headings")
        self.tree.heading("amount", text="Сумма")
        self.tree.heading("category", text="Категория")
        self.tree.heading("date", text="Дата")
        self.tree.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=5)

        # Кнопки управления
        self.btn_filter = tk.Button(root, text="Фильтровать", command=self.filter_expenses)
        self.btn_filter.grid(row=5, column=0, pady=5)

        self.btn_sum = tk.Button(root, text="Сумма за период", command=self.sum_period)
        self.btn_sum.grid(row=5, column=1, pady=5)

        self.btn_save = tk.Button(root, text="Сохранить в JSON", command=self.save_data)
        self.btn_save.grid(row=6, column=0, pady=5)

        # Загрузка данных при старте
        self.update_table()

    def load_data(self):
        if not os.path.exists(self.data_file):
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
            return []
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.expenses, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Сохранение", "Данные успешно сохранены!")

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for e in self.expenses:
            self.tree.insert("", "end", values=(e["amount"], e["category"], e["date"]))

    def add_expense(self):
        amount = self.entry_amount.get()
        category = self.entry_category.get()
        date = self.entry_date.get()

        # Валидация суммы
        if not (amount.replace('.', '', 1).isdigit() and float(amount) > 0):
            messagebox.showerror("Ошибка", "Сумма должна быть положительным числом")
            return

        # Валидация даты
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД")
            return

        self.expenses.append({
            "amount": float(amount),
            "category": category,
            "date": date
        })

        self.update_table()

    def filter_expenses(self):
        category = simpledialog.askstring("Фильтр", "Введите категорию (или оставьте пустым для всех):") or ""

        date_input = simpledialog.askstring("Фильтр", "Введите дату (ГГГГ-ММ-ДД) или оставьте пустым:") or ""

        filtered = []
        for e in self.expenses:
            cat_match = (category.lower() in e["category"].lower()) if category else True
            date_match = (e["date"] == date_input) if date_input else True
            if cat_match and date_match:
                filtered.append(e)

        for i in self.tree.get_children():
            self.tree.delete(i)

        for e in filtered:
            self.tree.insert("", "end", values=(e["amount"], e["category"], e["date"]))

    def sum_period(self):
        start_date = simpledialog.askstring("Период", "Введите начальную дату (ГГГГ-ММ-ДД):")
        end_date = simpledialog.askstring("Период", "Введите конечную дату (ГГГГ-ММ-ДД):")

        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")

            total = sum(
                e["amount"] for e in self.expenses
                if start <= datetime.strptime(e["date"], "%Y-%m-%d") <= end
            )

            messagebox.showinfo("Сумма", f"Сумма расходов за период: {total:.2f} руб.")

        except Exception as e:
            messagebox.showerror("Ошибка", "Некорректный формат даты или другие данные")


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()