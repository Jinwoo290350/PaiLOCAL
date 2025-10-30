@echo off
REM Plan My Trip API - Startup Script for Windows

echo 🚀 Starting Plan My Trip API...

REM Check if virtual environment exists
if not exist "venv\" (
    echo 📦 Creating virtual environment...
    python -m venv venv

    echo 📥 Installing dependencies...
    call venv\Scripts\activate
    pip install -r requirements.txt
) else (
    echo ✅ Virtual environment found
    call venv\Scripts\activate
)

echo 🌱 Starting server on http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo Press CTRL+C to stop the server
echo.

python app.py
