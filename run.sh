#!/bin/bash

# 의존성 설치
echo "의존성 설치 중..."
pip install -r requirements.txt

# 데이터베이스 초기화 (자동 생성됨)
echo "데이터베이스 초기화 중..."

# 서버 실행
echo "서버 시작 중..."
echo "브라우저에서 http://localhost:8000 으로 접속하세요"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000




