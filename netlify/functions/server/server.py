"""
Netlify 서버리스 함수용 FastAPI 래퍼
Mangum을 사용하여 FastAPI 앱을 AWS Lambda/Netlify Functions 형식으로 변환
"""
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
# server.py 위치: netlify/functions/server/server.py
# 프로젝트 루트까지: ../../.. (server -> functions -> netlify -> root)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 환경 변수 로드
from dotenv import load_dotenv
load_dotenv(os.path.join(project_root, '.env'))
load_dotenv(os.path.join(project_root, '.env.local'))

from mangum import Mangum
from app.main import app

# Mangum을 사용하여 FastAPI를 AWS Lambda/Netlify Functions 형식으로 변환
# lifespan="off"는 Netlify Functions의 제한을 고려한 설정
handler = Mangum(app, lifespan="off")

# Netlify Functions는 이 handler를 자동으로 인식합니다