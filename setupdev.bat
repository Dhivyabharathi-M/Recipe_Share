@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo   RecipeShare - Development Environment Setup
echo ============================================================
echo.

echo [1/5] Creating Python virtual environment...
cd backend
python -m venv env
if errorlevel 1 (
    echo ERROR: python not found. Install Python 3.10+.
    exit /b 1
)

echo [2/5] Installing Python dependencies...
call env\Scripts\activate
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: pip install failed.
    exit /b 1
)

echo [3/5] Running Alembic migrations...
alembic upgrade head
if errorlevel 1 (
    echo ERROR: Alembic migration failed.
    exit /b 1
)

echo [4/5] Seeding sample data...
python seed_data.py
if errorlevel 1 (
    echo WARNING: Seeding failed - continuing anyway.
)

cd ..

echo [5/5] Installing frontend dependencies...
cd frontend
npm install
if errorlevel 1 (
    echo ERROR: npm install failed. Install Node.js 18+.
    exit /b 1
)
cd ..

echo.
echo ============================================================
echo   Setup Complete! Run runapplication.bat to start the app.
echo ============================================================
endlocal
