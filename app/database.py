from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 환경 변수에서 데이터베이스 URL 가져오기 (Netlify 배포 시 외부 DB 사용)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./market_analytics.db")

# PostgreSQL URL 형식 변환 (Netlify 등에서 제공되는 형식)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# SQLite인 경우 - Netlify Functions 환경 고려
if DATABASE_URL.startswith("sqlite"):
    # Netlify Functions 환경 확인 (/tmp 디렉토리 사용 가능)
    if os.path.exists("/tmp") and not DATABASE_URL.startswith("sqlite:///:memory:"):
        # Netlify Functions 환경: /tmp 디렉토리 사용
        db_path = "/tmp/market_analytics.db"
        DATABASE_URL = f"sqlite:///{db_path}"
    elif DATABASE_URL == "sqlite:///./market_analytics.db":
        # 로컬 개발 환경: 상대 경로 사용
        pass
    
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    # PostgreSQL 등 다른 데이터베이스
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




