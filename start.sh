#!/bin/bash
# Railway 시작 스크립트

echo "Starting Application Market Analytics..."
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"
echo "PORT: ${PORT}"

# 의존성 확인
echo "Checking dependencies..."
python -c "import fastapi; print('FastAPI:', fastapi.__version__)"
python -c "import uvicorn; print('Uvicorn:', uvicorn.__version__)"

# 앱 시작
exec python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
