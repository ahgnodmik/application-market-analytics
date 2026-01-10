#!/usr/bin/env python3
"""
간단한 테스트 스크립트 - 앱이 정상적으로 시작되는지 확인
"""
import sys
import os

print("=" * 50)
print("Testing App Initialization")
print("=" * 50)

# 경로 확인
print(f"Current directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

# 의존성 확인
print("\nChecking dependencies...")
try:
    import fastapi
    print(f"✅ FastAPI: {fastapi.__version__}")
except Exception as e:
    print(f"❌ FastAPI: {e}")
    sys.exit(1)

try:
    import uvicorn
    print(f"✅ Uvicorn: {uvicorn.__version__}")
except Exception as e:
    print(f"❌ Uvicorn: {e}")
    sys.exit(1)

try:
    import sqlalchemy
    print(f"✅ SQLAlchemy: {sqlalchemy.__version__}")
except Exception as e:
    print(f"❌ SQLAlchemy: {e}")
    sys.exit(1)

# 앱 import 테스트
print("\nTesting app import...")
try:
    from app.main import app
    print("✅ App imported successfully")
    print(f"   App routes: {len(app.routes)} routes")
except Exception as e:
    print(f"❌ App import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 데이터베이스 테스트
print("\nTesting database...")
try:
    from app.database import engine, Base
    print("✅ Database modules imported")
except Exception as e:
    print(f"⚠️ Database import warning: {e}")

print("\n" + "=" * 50)
print("✅ All tests passed! App should work on Railway.")
print("=" * 50)
