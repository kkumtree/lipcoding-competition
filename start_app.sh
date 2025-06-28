#!/bin/bash

echo "🚀 Starting Mentor-Mentee Matching App"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run: python -m venv .venv"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Check if dependencies are installed
python -c "import fastapi" 2>/dev/null || {
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
}

echo "🔧 Starting Backend API Server (http://localhost:8080)..."
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 2

echo "🌐 Starting Frontend Server (http://localhost:3000)..."
python frontend_server.py &
FRONTEND_PID=$!

echo ""
echo "✅ Both servers are running!"
echo ""
echo "📱 Frontend App: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8080"
echo "📖 API Docs: http://localhost:8080/docs"
echo "📋 API Spec: http://localhost:8080/openapi.json"
echo ""
echo "Press Ctrl+C to stop both servers"

# Function to cleanup processes
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ All servers stopped"
}

# Set trap to cleanup on exit
trap cleanup EXIT

# Wait for user to stop
wait
