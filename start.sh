# Cleanup existing processes on ports 8000 and 8080
echo "Cleaning up existing processes..."
fuser -k 8000/tcp 8080/tcp 2>/dev/null || true
pkill -f "uvicorn backend.main:app" 2>/dev/null || true
pkill -f "http.server 8080" 2>/dev/null || true
sleep 1

# Start OrbitThink Chatbot - Backend and Frontend
echo "Starting backend server..."
cd /home/mehmam/Desktop/AI_Chatbot
./venv/bin/python3 -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

echo "Backend started (PID: $BACKEND_PID)"
echo "Starting frontend server..."
cd /home/mehmam/Desktop/AI_Chatbot/frontend
../venv/bin/python3 -m http.server 8080 &
FRONTEND_PID=$!

echo "Frontend started (PID: $FRONTEND_PID)"
echo ""
echo "================================"
echo "Chatbot is running!"
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:8080"
echo "================================"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait and handle Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
