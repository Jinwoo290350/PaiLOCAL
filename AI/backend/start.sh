#!/bin/bash

# Plan My Trip API - Startup Script

echo "🚀 Starting Plan My Trip API..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv

    echo "📥 Installing dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt
else
    echo "✅ Virtual environment found"
    source venv/bin/activate
fi

echo "🌱 Starting server on http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press CTRL+C to stop the server"
echo ""

python app.py
