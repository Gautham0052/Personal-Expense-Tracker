
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date

from database import (
    create_tables,
    add_transaction,
    get_transactions,
    update_transaction,
    delete_transaction,
    get_categories,
)

from dashboard import open_dashboard
from reports import open_monthly_report
from export import export_csv


class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Expense Tracker")
        self.root.geometry("1100x750")
        self.root.minsize(900, 650)
        self.root.resizable(True, True)

        self.selected_id = None

        self.build_ui()
        self.refresh_table()

    def build_ui(self):
        title = tk.Label(
            self.root,
            text="PERSONAL EXPENSE TRACKER",
            font=("Arial", 24, "bold"),
        )
        title.pack(pady=15)

        # Transaction Details
        form = tk.LabelFrame(
            self.root,
            text="Transaction Details",
            padx=15,
            pady=10,
        )
        form.pack(fill="x", padx=25, pady=5)

        tk.Label(form, text="Date:").grid(
            row=0, column=0, padx=8, pady=8, sticky="w"
        )

        self.date_entry = DateEntry(
            form,
            width=16,
            date_pattern="dd-mm-yyyy",
        )
        self.date_entry.grid(row=0, column=1, padx=8, pady=8)

        tk.Label(form, text="Type:").grid(
            row=0, column=2, padx=8, pady=8, sticky="w"
        )

        self.type_box = ttk.Combobox(
            form,
            values=("Expense", "Income"),
            state="readonly",
            width=17,
        )
        self.type_box.current(0)
        self.type_box.grid(row=0, column=3, padx=8, pady=8)

        tk.Label(form, text="Category:").grid(
            row=1, column=0, padx=8, pady=8, sticky="w"
        )

        categories = get_categories()

        self.category_box = ttk.Combobox(
            form,
            values=categories,
            state="readonly",
            width=17,
        )

        if categories:
            self.category_box.current(0)

        self.category_box.grid(row=1, column=1, padx=8, pady=8)

        tk.Label(form, text="Amount:").grid(
            row=1, column=2, padx=8, pady=8, sticky="w"
        )

        self.amount_entry = tk.Entry(form, width=20)
        self.amount_entry.grid(row=1, column=3, padx=8, pady=8)

        tk.Label(form, text="Description:").grid(
            row=2, column=0, padx=8, pady=8, sticky="w"
        )

        self.description_entry = tk.Entry(form, width=55)
        self.description_entry.grid(
            row=2,
            column=1,
            columnspan=3,
            padx=8,
            pady=8,
            sticky="ew",
        )

        # Transaction Buttons
        buttons = tk.Frame(self.root)
        buttons.pack(pady=10)

        self.add_button = tk.Button(
            buttons,
            text="ADD TRANSACTION",
            width=18,
            command=self.add,
        )
        self.add_button.grid(row=0, column=0, padx=4)

        self.update_button = tk.Button(
            buttons,
            text="UPDATE",
            width=12,
            command=self.update,
            state="disabled",
        )
        self.update_button.grid(row=0, column=1, padx=4)

        tk.Button(
            buttons,
            text="EDIT SELECTED",
            width=15,
            command=self.edit,
        ).grid(row=0, column=2, padx=4)

        tk.Button(
            buttons,
            text="DELETE SELECTED",
            width=17,
            command=self.delete,
        ).grid(row=0, column=3, padx=4)

        # Search and Filter
        search = tk.LabelFrame(
            self.root,
            text="Search & Filter",
            padx=10,
            pady=8,
        )
        search.pack(fill="x", padx=25, pady=5)

        tk.Label(search, text="Search:").grid(
            row=0, column=0, padx=5
        )

        self.search_entry = tk.Entry(search, width=22)
        self.search_entry.grid(row=0, column=1, padx=5)

        tk.Label(search, text="Category:").grid(
            row=0, column=2, padx=5
        )

        self.filter_category = ttk.Combobox(
            search,
            values=("All",) + tuple(categories),
            state="readonly",
            width=15,
        )
        self.filter_category.current(0)
        self.filter_category.grid(row=0, column=3, padx=5)

        tk.Label(search, text="Type:").grid(
            row=0, column=4, padx=5
        )

        self.filter_type = ttk.Combobox(
            search,
            values=("All", "Expense", "Income"),
            state="readonly",
            width=12,
        )
        self.filter_type.current(0)
        self.filter_type.grid(row=0, column=5, padx=5)

        tk.Button(
            search,
            text="SEARCH",
            width=10,
            command=self.search,
        ).grid(row=0, column=6, padx=5)

        tk.Button(
            search,
            text="CLEAR",
            width=10,
            command=self.clear_search,
        ).grid(row=0, column=7, padx=5)

        # Transaction Table
        table_frame = tk.Frame(self.root)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=10,
        )

        columns = (
            "id",
            "date",
            "type",
            "category",
            "description",
            "amount",
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=14,
        )

        headings = {
            "id": "ID",
            "date": "Date",
            "type": "Type",
            "category": "Category",
            "description": "Description",
            "amount": "Amount",
        }

        widths = {
            "id": 45,
            "date": 105,
            "type": 90,
            "category": 120,
            "description": 330,
            "amount": 120,
        }

        for col in columns:
            self.table.heading(col, text=headings[col])
            self.table.column(
                col,
                width=widths[col],
                anchor="center",
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview,
        )
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Summary
        self.summary_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 14, "bold"),
        )
        self.summary_label.pack(pady=5)

        # Dashboard, Reports, and Export
        bottom = tk.Frame(self.root)
        bottom.pack(pady=10)

        tk.Button(
            bottom,
            text="DASHBOARD",
            width=16,
            command=lambda: open_dashboard(self.root),
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            bottom,
            text="MONTHLY REPORT",
            width=18,
            command=lambda: open_monthly_report(self.root),
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            bottom,
            text="EXPORT CSV",
            width=16,
            command=self.export,
        ).grid(row=0, column=2, padx=5)

    def read_form(self):
        trans_date = self.date_entry.get()
        trans_type = self.type_box.get()
        category = self.category_box.get()
        description = self.description_entry.get().strip()
        amount_text = self.amount_entry.get().strip()

        if not trans_type or not category:
            messagebox.showwarning(
                "Missing Information",
                "Select a transaction type and category.",
            )
            return None

        if not description or not amount_text:
            messagebox.showwarning(
                "Missing Information",
                "Enter description and amount.",
            )
            return None

        try:
            amount = float(amount_text)
            if amount <= 0:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Invalid Amount",
                "Enter a valid positive number.",
            )
            return None

        return trans_date, trans_type, category, description, amount

    def add(self):
        data = self.read_form()
        if data is None:
            return

        try:
            add_transaction(*data)
            self.refresh_table()
            self.clear_form()

            messagebox.showinfo(
                "Success",
                "Transaction added successfully.",
            )

        except Exception as error:
            messagebox.showerror(
                "Database Error",
                f"Could not add transaction:\n{error}",
            )

    def edit(self):
        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Select a transaction first.",
            )
            return

        values = self.table.item(selected[0], "values")
        self.selected_id = int(values[0])

        self.date_entry.set_date(values[1])
        self.type_box.set(values[2])
        self.category_box.set(values[3])

        self.description_entry.delete(0, tk.END)
        self.description_entry.insert(0, values[4])

        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, values[5])

        self.add_button.config(state="disabled")
        self.update_button.config(state="normal")

    def update(self):
        if self.selected_id is None:
            return

        data = self.read_form()
        if data is None:
            return

        try:
            update_transaction(self.selected_id, *data)

            self.selected_id = None
            self.clear_form()
            self.add_button.config(state="normal")
            self.update_button.config(state="disabled")

            self.refresh_table()

            messagebox.showinfo(
                "Success",
                "Transaction updated successfully.",
            )

        except Exception as error:
            messagebox.showerror(
                "Database Error",
                f"Could not update transaction:\n{error}",
            )

    def delete(self):
        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Select a transaction first.",
            )
            return

        transaction_id = int(
            self.table.item(selected[0], "values")[0]
        )

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Delete the selected transaction?",
        )
        if not confirm:
            return

        try:
            delete_transaction(transaction_id)

            if self.selected_id == transaction_id:
                self.selected_id = None
                self.clear_form()
                self.add_button.config(state="normal")
                self.update_button.config(state="disabled")

            self.refresh_table()

            messagebox.showinfo(
                "Deleted",
                "Transaction deleted successfully.",
            )

        except Exception as error:
            messagebox.showerror(
                "Database Error",
                f"Could not delete transaction:\n{error}",
            )

    def refresh_table(self, transactions=None):
        if transactions is None:
            transactions = get_transactions()

        for item in self.table.get_children():
            self.table.delete(item)

        for row in transactions:
            self.table.insert(
                "",
                "end",
                values=(
                    row["id"],
                    row["date"],
                    row["type"],
                    row["category"],
                    row["description"],
                    f"{float(row['amount']):.2f}",
                ),
            )

        self.update_summary(transactions)

    def update_summary(self, transactions):
        expenses = sum(
            float(row["amount"])
            for row in transactions
            if row["type"] == "Expense"
        )

        income = sum(
            float(row["amount"])
            for row in transactions
            if row["type"] == "Income"
        )

        balance = income - expenses

        self.summary_label.config(
            text=(
                f"Income: ₹{income:.2f}    "
                f"Expenses: ₹{expenses:.2f}    "
                f"Balance: ₹{balance:.2f}"
            )
        )

    
    
    def search(self):
        search_text = self.search_entry.get().strip()
        category = self.filter_category.get()
        trans_type = self.filter_type.get()

        try:
            results = get_transactions(
                search=search_text,
                category=category,
                trans_type=trans_type,
            )

            self.refresh_table(results)

            if not results:
                messagebox.showinfo(
                    "Search Results",
                    "No matching transactions found.",
                )

        except Exception as error:
            messagebox.showerror(
                "Search Error",
                f"Could not search transactions:\n{error}",
            )



    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.filter_category.set("All")
        self.filter_type.set("All")
        self.refresh_table()

    def clear_form(self):
        self.amount_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)

        self.type_box.set("Expense")

        if self.category_box["values"]:
            self.category_box.current(0)

        # Reset to the actual current date
        self.date_entry.set_date(date.today())

    def export(self):
        try:
            path = export_csv()

            if path:
                messagebox.showinfo(
                    "Export Complete",
                    f"CSV exported to:\n{path}",
                )
            else:
                messagebox.showwarning(
                    "Export Cancelled",
                    "No export file was created.",
                )

        except Exception as error:
            messagebox.showerror(
                "Export Error",
                f"Could not export CSV:\n{error}",
            )


if __name__ == "__main__":
    create_tables()

    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
