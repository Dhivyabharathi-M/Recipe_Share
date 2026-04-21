"""seed_db.py – Run from inside the backend/ directory to seed sample recipes."""
import sqlite3
import os

db_path  = "recipes.db"
sql_path = os.path.join("..", "seed", "seed_data.sql")

if not os.path.exists(sql_path):
    print(f"ERROR: seed file not found at {sql_path}")
    raise SystemExit(1)

conn = sqlite3.connect(db_path)
with open(sql_path, "r") as f:
    conn.executescript(f.read())
conn.close()
print("Seed data inserted successfully.")
