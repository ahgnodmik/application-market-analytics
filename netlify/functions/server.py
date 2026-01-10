"""
Netlify 서버리스 함수용 FastAPI 래퍼
Mangum을 사용하여 FastAPI 앱을 AWS Lambda/Netlify Functions 형식으로 변환
"""
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
# server.py 위치: netlify/functions/server.py
# 프로젝트 루트까지: ../.. (functions -> netlify -> root)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 디버깅 정보 출력 (Netlify Functions 로그에서 확인 가능)
print(f"[Netlify Functions] Server.py location: {__file__}")
print(f"[Netlify Functions] Current dir: {current_dir}")
print(f"[Netlify Functions] Project root: {project_root}")
print(f"[Netlify Functions] Static exists: {os.path.exists(os.path.join(project_root, 'static'))}")
print(f"[Netlify Functions] Templates exists: {os.path.exists(os.path.join(project_root, 'templates'))}")

# 환경 변수 로드 (로컬 개발 환경에서만)
# Netlify에서는 환경 변수를 대시보드에서 설정해야 함
from dotenv import load_dotenv
env_file = os.path.join(project_root, '.env')
env_local_file = os.path.join(project_root, '.env.local')
if os.path.exists(env_file):
    load_dotenv(env_file)
if os.path.exists(env_local_file):
    load_dotenv(env_local_file)

from mangum import Mangum
from app.main import app

# Mangum을 사용하여 FastAPI를 AWS Lambda/Netlify Functions 형식으로 변환
# lifespan="off"는 Netlify Functions의 제한을 고려한 설정
handler = Mangum(app, lifespan="off")

# Netlify Functions는 이 handler를 자동으로 인식합니다
# 함수 이름은 디렉토리 이름 (server)
