
import sqlite3
import os

# ---------- Database Configuration ----------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "expenses.db")

CATEGORIES = (
    "Food",
    "Travel",
    "Shopping",
    "Bills",
    "Entertainment",
    "Education",
    "Health",
    "Other",
)


# ---------- Database Connection ----------

def connect():
    os.makedirs(DATA_DIR, exist_ok=True)
    return sqlite3.connect(DB_PATH)


# ---------- Create Tables ----------

def create_tables():
    connection = connect()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                type TEXT NOT NULL
                    CHECK(type IN ('Income', 'Expense')),
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY CHECK(id = 1),
                monthly_budget REAL NOT NULL DEFAULT 0
            )
        """)

        cursor.execute("""
            INSERT OR IGNORE INTO budgets (id, monthly_budget)
            VALUES (1, 0)
        """)

        connection.commit()

    finally:
        connection.close()


# ---------- Categories ----------

def get_categories():
    return CATEGORIES


# ---------- Add Transaction ----------

def add_transaction(date, trans_type, category, description, amount):
    connection = connect()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO transactions
                (date, type, category, description, amount)
            VALUES (?, ?, ?, ?, ?)
        """, (date, trans_type, category, description, amount))

        connection.commit()

    finally:
        connection.close()


# ---------- Get Transactions ----------

def get_transactions(search="", category="All", trans_type="All"):
    conn = connect()

    try:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        query = """
            SELECT id, date, type, category, description, amount
            FROM transactions
            WHERE 1=1
        """
        params = []

        if search:
            query += """
                AND (
                    date LIKE ?
                    OR description LIKE ?
                    OR category LIKE ?
                    OR type LIKE ?
                )
            """
            pattern = f"%{search}%"
            params.extend([pattern, pattern, pattern, pattern])

        if category and category != "All":
            query += " AND category = ?"
            params.append(category)

        if trans_type and trans_type != "All":
            query += " AND type = ?"
            params.append(trans_type)

        query += " ORDER BY id DESC"

        cursor.execute(query, params)
        return cursor.fetchall()

    finally:
        conn.close()
# ---------- Update Transaction ----------

def update_transaction(
    transaction_id,
    date,
    trans_type,
    category,
    description,
    amount,
):
    connection = connect()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE transactions
            SET date = ?,
                type = ?,
                category = ?,
                description = ?,
                amount = ?
            WHERE id = ?
        """, (
            date,
            trans_type,
            category,
            description,
            amount,
            transaction_id,
        ))

        connection.commit()

    finally:
        connection.close()


# ---------- Delete Transaction ----------

def delete_transaction(transaction_id):
    connection = connect()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM transactions WHERE id = ?",
            (transaction_id,),
        )

        connection.commit()

    finally:
        connection.close()


# ---------- Balance Summary ----------

def get_balance_summary():
    connection = connect()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                COALESCE(
                    SUM(CASE WHEN type = 'Income'
                        THEN amount ELSE 0 END), 0
                ),
                COALESCE(
                    SUM(CASE WHEN type = 'Expense'
                        THEN amount ELSE 0 END), 0
                ),
                COUNT(*)
            FROM transactions
        """)

        income, expenses, count = cursor.fetchone()

        cursor.execute("""
            SELECT monthly_budget
            FROM budgets
            WHERE id = 1
        """)

        result = cursor.fetchone()
        budget = result[0] if result else 0

        return {
            "income": income,
            "expenses": expenses,
            "balance": income - expenses,
            "count": count,
            "budget": budget,
        }

    finally:
        connection.close()


# ---------- Category Totals ----------

def get_category_totals(trans_type="Expense"):
    connection = connect()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT category, SUM(amount)
            FROM transactions
            WHERE type = ?
            GROUP BY category
            ORDER BY SUM(amount) DESC
        """, (trans_type,))

        return cursor.fetchall()

    finally:
        connection.close()


# ---------- Monthly Totals ----------

def get_monthly_totals(year, trans_type="Expense"):
    connection = connect()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT substr(date, 4, 2), SUM(amount)
            FROM transactions
            WHERE substr(date, 7, 4) = ?
              AND type = ?
            GROUP BY substr(date, 4, 2)
            ORDER BY substr(date, 4, 2)
        """, (str(year), trans_type))

        return cursor.fetchall()

    finally:
        connection.close()


# ---------- Month Category Totals ----------

def get_month_category_totals(month, year):
    connection = connect()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT category, SUM(amount)
            FROM transactions
            WHERE substr(date, 4, 2) = ?
              AND substr(date, 7, 4) = ?
              AND type = 'Expense'
            GROUP BY category
            ORDER BY SUM(amount) DESC
        """, (f"{int(month):02d}", str(year)))

        return cursor.fetchall()

    finally:
        connection.close()


# ---------- Get Budget ----------

def get_budget():
    connection = connect()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT monthly_budget
            FROM budgets
            WHERE id = 1
        """)

        result = cursor.fetchone()
        return result[0] if result else 0

    finally:
        connection.close()


# ---------- Set Budget ----------

def set_budget(amount):
    amount = float(amount)

    if amount < 0:
        raise ValueError("Budget cannot be negative.")

    connection = connect()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE budgets
            SET monthly_budget = ?
            WHERE id = 1
        """, (amount,))

        connection.commit()

    finally:
        connection.close()


# ---------- Run Directly to Initialize Database ----------

if __name__ == "__main__":
    create_tables()
    print("Database and tables created successfully.")
    print("Database location:", DB_PATH)
