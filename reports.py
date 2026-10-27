
import tkinter as tk
from tkinter import ttk, messagebox

from database import get_month_category_totals, get_monthly_totals

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def open_monthly_report(parent):
    report = tk.Toplevel(parent)
    report.title("Monthly Expense Report")
    report.geometry("750x620")
    report.resizable(False, False)

    tk.Label(
        report,
        text="MONTHLY EXPENSE REPORT",
        font=("Arial", 22, "bold"),
    ).pack(pady=15)

    # ---------- Month and Year Controls ----------
    controls = tk.Frame(report)
    controls.pack(pady=5)

    tk.Label(controls, text="Month:").grid(
        row=0, column=0, padx=5
    )

    month_box = ttk.Combobox(
        controls,
        values=tuple(str(i) for i in range(1, 13)),
        state="readonly",
        width=10,
    )
    month_box.current(0)
    month_box.grid(row=0, column=1, padx=5)

    tk.Label(controls, text="Year:").grid(
        row=0, column=2, padx=5
    )

    year_entry = tk.Entry(controls, width=10)
    year_entry.insert(0, "2026")
    year_entry.grid(row=0, column=3, padx=5)

    # ---------- Report Table ----------
    table = ttk.Treeview(
        report,
        columns=("category", "amount"),
        show="headings",
        height=10,
    )

    table.heading("category", text="Category")
    table.heading("amount", text="Amount")

    table.column("category", width=280)
    table.column("amount", width=220)

    table.pack(pady=20)

    total_label = tk.Label(
        report,
        text="Total Expenses: ₹0.00",
        font=("Arial", 14, "bold"),
    )
    total_label.pack(pady=5)

    # ---------- Generate Report ----------
    def generate():
        for item in table.get_children():
            table.delete(item)

        try:
            month = int(month_box.get())
            year = int(year_entry.get().strip())

            if month < 1 or month > 12 or year < 1:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Invalid Input",
                "Enter a valid month and year.",
                parent=report,
            )
            return

        try:
            rows = get_month_category_totals(month, year)
            total = 0.0

            for category, amount in rows:
                amount = float(amount)

                table.insert(
                    "",
                    "end",
                    values=(category, f"₹{amount:.2f}"),
                )

                total += amount

            total_label.config(
                text=f"Total Expenses: ₹{total:.2f}"
            )

            update_chart(year)

        except Exception as error:
            messagebox.showerror(
                "Report Error",
                f"Could not generate report:\n{error}",
                parent=report,
            )

    tk.Button(
        controls,
        text="GENERATE REPORT",
        command=generate,
    ).grid(row=0, column=4, padx=10)

    # ---------- Monthly Bar Chart ----------
    chart_frame = tk.Frame(report)
    chart_frame.pack(pady=10)

    figure = Figure(figsize=(6.7, 2.8), dpi=100)
    axis = figure.add_subplot(111)

    canvas = FigureCanvasTkAgg(figure, master=chart_frame)
    canvas.get_tk_widget().pack()

    def update_chart(year):
        axis.clear()

        months = [str(i) for i in range(1, 13)]
        rows = get_monthly_totals(year, "Expense")

        values = {
            str(int(month)): float(amount)
            for month, amount in rows
        }

        amounts = [values.get(month, 0) for month in months]

        axis.bar(months, amounts)
        axis.set_title(f"Monthly Expenses - {year}")
        axis.set_xlabel("Month")
        axis.set_ylabel("Amount")

        figure.tight_layout()
        canvas.draw()

    # Display the initial chart for the default year.
    update_chart(2026)
