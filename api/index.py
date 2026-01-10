"""
Vercel Serverless Functions 엔트리 포인트
FastAPI 앱을 Vercel Functions로 실행
"""
from mangum import Mangum
import sys
import os

# 프로젝트 루트를 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# FastAPI 앱 import
from app.main import app

# Mangum으로 ASGI 앱을 Lambda/API Gateway 형식으로 변환
handler = Mangum(app, lifespan="off")

# Vercel은 handler를 직접 호출
__all__ = ["handler"]
