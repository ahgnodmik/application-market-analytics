"""
Netlify 서버리스 함수용 FastAPI 래퍼
Mangum을 사용하여 FastAPI 앱을 AWS Lambda/Netlify Functions 형식으로 변환
"""
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
# server.py 위치: netlify/functions/server.py
# Netlify Functions 환경에서는:
# - server.py와 같은 디렉토리에 app/, templates/, static/이 있음 (빌드 시 복사됨)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../..'))
functions_dir = current_dir  # netlify/functions/

# Functions 디렉토리에 app이 있으면 우선 사용 (빌드 시 복사됨)
if os.path.exists(os.path.join(functions_dir, 'app')):
    if functions_dir not in sys.path:
        sys.path.insert(0, functions_dir)
    print(f"[Netlify Functions] ✅ Using app from functions directory: {functions_dir}")
    print(f"[Netlify Functions] App directory exists: {os.path.exists(os.path.join(functions_dir, 'app'))}")
else:
    # 프로젝트 루트 사용 (로컬 개발 환경)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    print(f"[Netlify Functions] Using app from project root: {project_root}")
    print(f"[Netlify Functions] App directory exists: {os.path.exists(os.path.join(project_root, 'app'))}")

# 디버깅 정보 출력 (Netlify Functions 로그에서 확인 가능)
print(f"[Netlify Functions] Server.py location: {__file__}")
print(f"[Netlify Functions] Current dir: {current_dir}")
print(f"[Netlify Functions] Project root: {project_root}")
print(f"[Netlify Functions] Working directory: {os.getcwd()}")
print(f"[Netlify Functions] Static exists: {os.path.exists(os.path.join(project_root, 'static'))}")
print(f"[Netlify Functions] Templates exists: {os.path.exists(os.path.join(project_root, 'templates'))}")

# Lambda/Netlify Functions 환경 변수 확인
print(f"[Netlify Functions] LAMBDA_TASK_ROOT: {os.environ.get('LAMBDA_TASK_ROOT', 'Not set')}")
print(f"[Netlify Functions] _HANDLER: {os.environ.get('_HANDLER', 'Not set')}")

# 환경 변수 로드 (로컬 개발 환경에서만)
# Netlify에서는 환경 변수를 대시보드에서 설정해야 함
try:
    from dotenv import load_dotenv
    env_file = os.path.join(project_root, '.env')
    env_local_file = os.path.join(project_root, '.env.local')
    if os.path.exists(env_file):
        load_dotenv(env_file)
        print(f"[Netlify Functions] Loaded .env from {env_file}")
    if os.path.exists(env_local_file):
        load_dotenv(env_local_file)
        print(f"[Netlify Functions] Loaded .env.local from {env_local_file}")
except Exception as e:
    print(f"[Netlify Functions] Error loading .env files: {e}")

# FastAPI 앱 import 및 에러 핸들링
try:
    from mangum import Mangum
    from app.main import app
    
    print(f"[Netlify Functions] FastAPI app imported successfully")
    print(f"[Netlify Functions] App routes: {[r.path for r in app.routes[:5]]}")
    
    # Mangum을 사용하여 FastAPI를 AWS Lambda/Netlify Functions 형식으로 변환
    # lifespan="off"는 Netlify Functions의 제한을 고려한 설정
    handler = Mangum(app, lifespan="off")
    
    print(f"[Netlify Functions] Mangum handler created successfully")
    print(f"[Netlify Functions] Handler type: {type(handler)}")
    
except Exception as e:
    import traceback
    print(f"[Netlify Functions] CRITICAL ERROR importing app: {e}")
    print(f"[Netlify Functions] Traceback: {traceback.format_exc()}")
    # 에러 핸들러 함수 생성
    def handler(event, context):
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': f'{{"error": "Failed to initialize app: {str(e)}"}}'
        }
    raise

# Netlify Functions는 이 handler를 자동으로 인식합니다
# 함수 이름은 디렉토리 이름 (server)
