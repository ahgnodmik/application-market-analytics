#!/bin/bash
# Railway 시작 스크립트

echo "Starting Application Market Analytics..."
echo "Current directory: $(pwd)"
echo "Python version: $(python3 --version 2>&1 || echo 'Python3 not found')"
echo "PORT: ${PORT}"

# 의존성 확인
echo "Checking dependencies..."
python3 -c "import fastapi; print('FastAPI:', fastapi.__version__)" 2>&1 || echo "FastAPI check failed"
python3 -c "import uvicorn; print('Uvicorn:', uvicorn.__version__)" 2>&1 || echo "Uvicorn check failed"

# 앱 시작
exec python3 -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
