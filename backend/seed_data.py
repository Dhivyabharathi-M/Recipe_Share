"""
seed_data.py
Run from inside the backend/ folder:
    python seed_data.py
Inserts 10 sample recipes into recipes.db (skips if already seeded).
"""
import sqlite3
import os

DB_PATH  = "recipes.db"
SQL_PATH = os.path.join("..", "seed", "seed_data.sql")


def main():
    if not os.path.exists(DB_PATH):
        print(f"ERROR: {DB_PATH} not found. Run 'alembic upgrade head' first.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if already seeded
    cursor.execute("SELECT COUNT(*) FROM recipes")
    count = cursor.fetchone()[0]
    if count > 0:
        print(f"Database already has {count} recipes. Skipping seed.")
        conn.close()
        return

    # Read and execute SQL
    sql_path = os.path.abspath(SQL_PATH)
    if not os.path.exists(sql_path):
        print(f"ERROR: seed file not found at {sql_path}")
        conn.close()
        return

    with open(sql_path, "r", encoding="utf-8") as f:
        sql = f.read()

    conn.executescript(sql)
    conn.close()

    print("Seed data inserted successfully (10 sample recipes).")


if __name__ == "__main__":
    main()
