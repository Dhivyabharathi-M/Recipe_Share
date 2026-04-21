#!/usr/bin/env bash
set -e

echo "============================================================"
echo "  RecipeShare - Development Environment Setup (macOS/Linux)"
echo "============================================================"

# ── Backend ────────────────────────────────────────────────────
echo "[1/5] Creating Python virtual environment..."
cd backend
python3 -m venv env

echo "[2/5] Installing Python dependencies..."
source env/bin/activate
pip install -r requirements.txt

echo "[3/5] Running Alembic migrations..."
alembic upgrade head

echo "[4/5] Seeding sample data..."
python3 -c "
import sqlite3, os
conn = sqlite3.connect('recipes.db')
with open(os.path.join('..','seed','seed_data.sql')) as f:
    conn.executescript(f.read())
conn.close()
print('Seed data inserted.')
"

cd ..

# ── Frontend ───────────────────────────────────────────────────
echo "[5/5] Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo ""
echo "============================================================"
echo "  Setup complete! Run ./runapplication.sh to start."
echo "============================================================"
