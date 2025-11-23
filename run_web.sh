# 🚀 Complete ADAS System - Quick Start Script
# This script starts both backend and frontend servers

echo "====================================="
echo "🚗 Starting ADAS System"
echo "====================================="
echo ""

# Set Gemini API Key
export GEMINI_API_KEY="AIzaSyBtICNdgK73KkXLi2kyzUY7NxJbvp_0zRY"

echo "✅ Gemini API Key set"
echo ""

# Check if MySQL is running (optional - system works without it)
if ! mysql -u root -pAnurag*29 -e "SELECT 1" &> /dev/null; then
    echo "⚠️  MySQL not running - using local camera mode"
    echo "   (This is OK! System will still work)"
else
    echo "✅ MySQL connected"
fi

echo ""
echo "🔧 Starting Backend (FastAPI + AI)..."
echo "   URL: http://localhost:8000"
echo ""

# Start backend in background
GEMINI_API_KEY="$GEMINI_API_KEY" python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

echo "🎨 Starting Frontend (React)..."
echo "   URL: http://localhost:5173"
echo ""

# Start frontend
cd frontend && npm run dev -- --host &
FRONTEND_PID=$!

# Wait a bit
sleep 2

echo ""
echo "====================================="
echo "✅ ADAS System is Running!"
echo "====================================="
echo ""
echo "📊 Backend:  http://localhost:8000"
echo "🌐 Frontend: http://localhost:5173"
echo ""
echo "🚀 Opening dashboard in browser..."
sleep 2
open http://localhost:5173

echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Wait for user interrupt
wait
