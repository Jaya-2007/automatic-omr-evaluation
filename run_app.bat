@echo off
REM Kill all old Python processes
taskkill /F /IM python.exe >nul 2>&1

REM Start backend (FastAPI) on port 8000
start cmd /k "python -m uvicorn backend:app --reload --port 8000"

REM Start frontend (Streamlit) on port 8503
start cmd /k "python -m streamlit run app.py --server.port 8503"

echo.
echo Backend and frontend started!
echo Frontend URL: http://localhost:8503
echo Backend URL: http://localhost:8000
pause
