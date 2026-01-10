"""
Vercel Serverless Functions 엔트리 포인트
"""
import sys
import os

# 프로젝트 루트를 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 환경 변수 로드
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

try:
    from mangum import Mangum
    from app.main import app
    handler = Mangum(app, lifespan="off")
except Exception as e:
    def handler(event, context):
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': f'{{"error": "Failed to initialize: {str(e)}"}}'
        }
