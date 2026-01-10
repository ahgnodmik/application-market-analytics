#!/usr/bin/env python3
"""
Railway 시작 스크립트
앱이 정상적으로 시작되는지 확인하고 시작
"""
import os
import sys

# 즉시 출력 (버퍼링 없음)
sys.stdout.flush()
sys.stderr.flush()

print("=" * 60)
print("🚀 Starting Application Market Analytics")
print("=" * 60)

# 포트 확인
port = os.getenv('PORT', '8000')
print(f"PORT environment variable: {port}")
print(f"Current directory: {os.getcwd()}")
print(f"Python path: {sys.path[:3]}")
sys.stdout.flush()

# 앱 import 및 시작
try:
    print("Importing app...")
    sys.stdout.flush()
    
    from app.main import app
    import uvicorn
    
    print("✅ App imported successfully")
    print(f"   App title: {app.title}")
    print(f"   Routes count: {len(app.routes)}")
    sys.stdout.flush()
    
    # uvicorn 시작
    print(f"Starting uvicorn on 0.0.0.0:{port}...")
    sys.stdout.flush()
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(port),
        log_level="info",
        access_log=True
    )
except Exception as e:
    print(f"❌ ERROR: {e}")
    sys.stdout.flush()
    import traceback
    traceback.print_exc()
    sys.stderr.flush()
    sys.exit(1)
