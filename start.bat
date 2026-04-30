@echo off
echo ============================================================
echo  UK House Price Predictor - Startup Script
echo ============================================================

:: ── Install backend deps ─────────────────────────────────────
echo.
echo [1/4] Installing Python backend dependencies...
cd backend
python -m pip install -r requirements.txt --quiet
cd ..

:: ── Install frontend deps ────────────────────────────────────
echo [2/4] Installing Node.js frontend dependencies...
cd frontend
call npm install --silent
cd ..

:: ── Start backend ────────────────────────────────────────────
echo [3/4] Starting Flask backend (http://localhost:5000) ...
start "Flask Backend" cmd /k "cd backend && python app.py"

:: ── Start frontend ───────────────────────────────────────────
echo [4/4] Starting React frontend (http://localhost:5173) ...
timeout /t 3 /nobreak >nul
start "React Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ============================================================
echo  Open http://localhost:5173 in your browser
echo ============================================================
pause
