
# My Personal Expense Tracker 

A desktop application built with Python, Tkinter, and SQLite to manage personal income and expenses. The application allows users to add, edit, delete, search, filter, and export financial transactions.

## Features

- **Add Transactions:** Record income and expenses with date, category, amount, and description.
- **View Transactions:** Display all transactions in a table.
- **Edit Transactions:** Update existing transaction details.
- **Delete Transactions:** Remove selected transactions.
- **Search Transactions:** Search by date, description, category, or transaction type.
- **Filter Transactions:** Filter records by category and type.
- **Dashboard:** View income, expenses, balance, category charts, and budget information.
- **Monthly Reports:** Generate monthly expense reports and visual charts.
- **CSV Export:** Export transaction records to a CSV file for use in Excel or other spreadsheet applications.
- **SQLite Database:** Store transaction data locally.

## Technologies Used

- Python 3
- Tkinter — graphical user interface
- SQLite — database management
- tkcalendar — date picker
- Matplotlib — charts and visual reports
- CSV — transaction data export

## Project Structure

```text
Projects/
├── main.py
├── database.py
├── dashboard.py
├── reports.py
├── export.py
├── README.md
├── data/
│   └── expenses.db
└── expense_report.csv
```

**Note:** The database and CSV files are generated or used by the application. You do not need to create the CSV file manually.

## Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd YOUR_PROJECT_FOLDER
```

Replace the placeholders with your actual GitHub repository URL and folder name.

### 2. Install dependencies

```bash
python -m pip install tkcalendar matplotlib
```

If you are using Anaconda on macOS, run:

```bash
/opt/anaconda3/bin/python -m pip install tkcalendar matplotlib
```

### 3. Run the application

```bash
python main.py
```

For the Anaconda installation on macOS:

```bash
/opt/anaconda3/bin/python main.py
```

Make sure all five Python files are in the same project directory.

## How to Use

1. Run `main.py` to open the application.
2. Select a transaction date.
3. Choose **Income** or **Expense**.
4. Select a category.
5. Enter the amount and description.
6. Click **ADD TRANSACTION** to save the record.
7. Select a transaction and click **EDIT SELECTED** to modify it.
8. Select a transaction and click **DELETE SELECTED** to remove it.
9. Use the search field and category/type filters to find transactions.
10. Click **CLEAR** to remove search filters and display all transactions.
11. Open **DASHBOARD** to view financial summaries and charts.
12. Open **MONTHLY REPORT** to view monthly expense information.
13. Click **EXPORT CSV** to export transactions.

## Data Storage

Transaction records are stored in the SQLite database:

```text
data/expenses.db
```

The CSV export is saved as:

```text
expense_report.csv
```

The exported file contains transaction ID, date, type, category, description, and amount.

Dates use the `DD-MM-YYYY` format, and monetary values are displayed in Indian rupees (₹).

## Troubleshooting

### ModuleNotFoundError: No module named 'tkcalendar'

Install the dependency using the same Python interpreter used to run the application:

```bash
python -m pip install tkcalendar
```

### ModuleNotFoundError: No module named 'matplotlib'

Install Matplotlib:

```bash
python -m pip install matplotlib
```

### Transactions are not appearing

- Ensure all required fields are filled in.
- Enter a valid positive amount.
- Check the selected category and transaction type filters.
- Click **CLEAR** to display all transactions.

### CSV export is not working

Ensure the application has permission to write to the project folder. Click **EXPORT CSV** to create the CSV file.

## Future Enhancements

- Recurring income and expense tracking
- Custom transaction categories
- Budget alerts and notifications
- Additional financial charts
- Monthly and yearly savings analysis
- Database backup and restore functionality
