@echo off
setlocal

echo ============================================================
echo   RecipeShare - Starting Application
echo ============================================================
echo.
echo   Backend  ^>  http://localhost:8000
echo   Swagger  ^>  http://localhost:8000/docs
echo   Frontend ^>  http://localhost:3000
echo.

REM ── Start FastAPI backend in a new window ─────────────────────
echo Starting FastAPI backend...
start "RecipeShare Backend" cmd /k "cd /d %~dp0backend && call env\Scripts\activate && python main.py"

REM ── Wait a moment then start frontend ─────────────────────────
timeout /t 3 /nobreak >nul

REM ── Start React frontend in a new window ──────────────────────
echo Starting React frontend...
start "RecipeShare Frontend" cmd /k "cd /d %~dp0frontend && npm start"

echo.
echo Both servers starting in separate windows.
echo Close those windows to stop the servers.
endlocal
