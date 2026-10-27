
import csv
import os
from database import get_transactions


def export_csv():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, "expense_report.csv")

    rows = get_transactions()

    try:
        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow([
                "ID",
                "Date",
                "Type",
                "Category",
                "Description",
                "Amount"
            ])

            for row in rows:
                writer.writerow([
                    row["id"],
                    row["date"],
                    row["type"],
                    row["category"],
                    row["description"],
                    row["amount"]
                ])

        return path

    except (OSError, KeyError, TypeError) as error:
        raise RuntimeError(f"Failed to export expenses: {error}") from error
