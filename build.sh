#!/bin/bash
# Netlify 빌드 스크립트

set -e

echo "🔧 Installing Python dependencies..."

# Python 버전 확인
python3.9 --version || python3 --version

# pip 업그레이드
python3.9 -m pip install --upgrade pip || python3 -m pip install --upgrade pip

# 의존성 설치
python3.9 -m pip install -r requirements.txt || python3 -m pip install -r requirements.txt

echo "✅ Dependencies installed successfully"

