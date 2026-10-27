
import tkinter as tk
from tkinter import messagebox

from database import (
    get_balance_summary,
    get_category_totals,
    set_budget,
)

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def open_dashboard(parent):
    dashboard = tk.Toplevel(parent)
    dashboard.title("Expense Dashboard")
    dashboard.geometry("900x720")
    dashboard.resizable(False, False)

    tk.Label(
        dashboard,
        text="EXPENSE DASHBOARD",
        font=("Arial", 24, "bold"),
    ).pack(pady=15)

    summary = get_balance_summary()

    # Summary cards
    cards = tk.Frame(dashboard)
    cards.pack(pady=5)

    card_data = [
        ("TOTAL INCOME", f"₹{summary['income']:.2f}"),
        ("TOTAL EXPENSES", f"₹{summary['expenses']:.2f}"),
        ("BALANCE", f"₹{summary['balance']:.2f}"),
        ("TRANSACTIONS", str(summary["count"])),
    ]

    for i, (title, value) in enumerate(card_data):
        frame = tk.LabelFrame(
            cards,
            text=title,
            padx=25,
            pady=12,
        )
        frame.grid(row=0, column=i, padx=6)

        tk.Label(
            frame,
            text=value,
            font=("Arial", 15, "bold"),
        ).pack()

    # Monthly budget
    budget_frame = tk.LabelFrame(
        dashboard,
        text="Monthly Budget",
        padx=15,
        pady=10,
    )
    budget_frame.pack(pady=10)

    budget = float(summary.get("budget", 0) or 0)

    tk.Label(
        budget_frame,
        text=f"Current Budget: ₹{budget:.2f}",
    ).grid(row=0, column=0, padx=8)

    budget_entry = tk.Entry(budget_frame, width=15)
    budget_entry.grid(row=0, column=1, padx=8)

    def save_budget():
        try:
            value = float(budget_entry.get().strip())

            if value < 0:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Invalid Budget",
                "Enter a valid non-negative number.",
                parent=dashboard,
            )
            return

        try:
            set_budget(value)

            messagebox.showinfo(
                "Budget",
                "Monthly budget saved successfully.",
                parent=dashboard,
            )

            dashboard.destroy()
            open_dashboard(parent)

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Could not save budget:\n{error}",
                parent=dashboard,
            )

    tk.Button(
        budget_frame,
        text="SAVE BUDGET",
        command=save_budget,
    ).grid(row=0, column=2, padx=8)

    # Budget usage
    if budget > 0:
        remaining = budget - summary["expenses"]
        percent = (summary["expenses"] / budget) * 100

        tk.Label(
            dashboard,
            text=(
                f"Budget Used: {percent:.1f}% "
                f"Remaining: ₹{remaining:.2f}"
            ),
            font=("Arial", 12, "bold"),
        ).pack(pady=5)

        if percent >= 100:
            tk.Label(
                dashboard,
                text="Warning: You have exceeded your budget!",
                font=("Arial", 13, "bold"),
                fg="red",
            ).pack(pady=5)

        elif percent >= 80:
            tk.Label(
                dashboard,
                text="Warning: You have used 80% or more of your budget.",
                font=("Arial", 13, "bold"),
                fg="orange",
            ).pack(pady=5)

    # Expense category chart
    category_data = get_category_totals("Expense")

    if not category_data:
        tk.Label(
            dashboard,
            text="No expense data available for the chart.",
            font=("Arial", 13),
        ).pack(pady=40)
        return

    categories = [row[0] for row in category_data]
    amounts = [float(row[1]) for row in category_data]

    # A pie chart requires positive values
    chart_data = [
        (category, amount)
        for category, amount in zip(categories, amounts)
        if amount > 0
    ]

    if not chart_data:
        tk.Label(
            dashboard,
            text="No positive expense data available for the chart.",
            font=("Arial", 13),
        ).pack(pady=40)
        return

    categories = [row[0] for row in chart_data]
    amounts = [row[1] for row in chart_data]

    figure = Figure(figsize=(7.2, 4.1), dpi=100)
    axis = figure.add_subplot(111)

    axis.pie(
        amounts,
        labels=categories,
        autopct="%1.1f%%",
    )

    axis.set_title("Expenses by Category")

    canvas = FigureCanvasTkAgg(figure, master=dashboard)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)
