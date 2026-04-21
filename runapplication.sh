#!/usr/bin/env bash
set -e

echo "Starting RecipeShare..."
echo "Backend  → http://localhost:8000"
echo "Swagger  → http://localhost:8000/docs"
echo "Frontend → http://localhost:3000"
echo ""

# Start backend
cd backend
source env/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to bind
sleep 2

# Start frontend
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo "Backend PID:  $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "Press Ctrl+C to stop both."

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo 'Stopped.'" INT TERM
wait $BACKEND_PID $FRONTEND_PID
