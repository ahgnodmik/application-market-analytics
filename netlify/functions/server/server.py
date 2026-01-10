"""
Netlify 서버리스 함수용 FastAPI 래퍼
Mangum을 사용하여 FastAPI 앱을 AWS Lambda/Netlify Functions 형식으로 변환
"""
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
# server.py 위치: netlify/functions/server/server.py
# Netlify Functions 환경에서는:
# - netlify/functions/ 디렉토리에 app/, templates/, static/이 있음 (빌드 시 복사됨)
current_dir = os.path.dirname(os.path.abspath(__file__))  # netlify/functions/server
functions_root = os.path.dirname(current_dir)  # netlify/functions
project_root = os.path.dirname(functions_root)  # 프로젝트 루트

# Functions 디렉토리에 app이 있으면 우선 사용 (빌드 시 복사됨)
functions_app_dir = os.path.join(functions_root, 'app')
if os.path.exists(functions_app_dir):
    if functions_root not in sys.path:
        sys.path.insert(0, functions_root)
    print(f"[Server] ✅ Using app from functions directory: {functions_app_dir}")
else:
    # 프로젝트 루트 사용 (로컬 개발 환경)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    print(f"[Server] Using app from project root: {project_root}")
    print(f"[Server] App directory exists: {os.path.exists(os.path.join(project_root, 'app'))}")

# 디버깅 정보 출력 (Netlify Functions 로그에서 확인 가능)
print(f"[Server] Server.py location: {__file__}")
print(f"[Server] Current dir: {current_dir}")
print(f"[Server] Functions root: {functions_root}")
print(f"[Server] Project root: {project_root}")
print(f"[Server] Working directory: {os.getcwd()}")
print(f"[Server] Static exists in functions: {os.path.exists(os.path.join(functions_root, 'static'))}")
print(f"[Server] Templates exists in functions: {os.path.exists(os.path.join(functions_root, 'templates'))}")

# Lambda/Netlify Functions 환경 변수 확인
print(f"[Server] LAMBDA_TASK_ROOT: {os.environ.get('LAMBDA_TASK_ROOT', 'Not set')}")
print(f"[Server] _HANDLER: {os.environ.get('_HANDLER', 'Not set')}")

# 환경 변수 로드 (로컬 개발 환경에서만)
# Netlify에서는 환경 변수를 대시보드에서 설정해야 함
try:
    from dotenv import load_dotenv
    env_file = os.path.join(project_root, '.env')
    env_local_file = os.path.join(project_root, '.env.local')
    if os.path.exists(env_file):
        load_dotenv(env_file)
        print(f"[Server] Loaded .env from {env_file}")
    if os.path.exists(env_local_file):
        load_dotenv(env_local_file)
        print(f"[Server] Loaded .env.local from {env_local_file}")
except Exception as e:
    print(f"[Server] Error loading .env files: {e}")

# FastAPI 앱 import 및 에러 핸들링
try:
    from mangum import Mangum
    from app.main import app
    
    print(f"[Server] ✅ FastAPI app imported successfully")
    print(f"[Server] App routes: {[r.path for r in app.routes[:5]]}")
    
    # Mangum을 사용하여 FastAPI를 AWS Lambda/Netlify Functions 형식으로 변환
    # lifespan="off"는 Netlify Functions의 제한을 고려한 설정
    handler = Mangum(app, lifespan="off")
    
    print(f"[Server] ✅ Mangum handler created successfully")
    print(f"[Server] Handler type: {type(handler)}")
    
except Exception as e:
    import traceback
    print(f"[Server] ❌ CRITICAL ERROR importing app: {e}")
    print(f"[Server] Traceback: {traceback.format_exc()}")
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
