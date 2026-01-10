#!/usr/bin/env python3
"""
Railway 시작 스크립트
앱이 정상적으로 시작되는지 확인하고 시작
"""
import os
import sys

# 포트 확인
port = os.getenv('PORT', '8000')
print(f"Starting on port: {port}")

# 앱 import 및 시작
try:
    from app.main import app
    import uvicorn
    
    print("✅ App imported successfully")
    print(f"   Routes: {len(app.routes)}")
    
    # uvicorn 시작
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(port),
        log_level="info"
    )
except Exception as e:
    print(f"❌ Error starting app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
