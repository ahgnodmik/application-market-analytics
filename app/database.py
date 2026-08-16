from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# 데이터베이스 URL 설정 (설정 모듈 사용 - 기획서 16.1)
DATABASE_URL = settings.DATABASE_URL or settings.database_url_sqlite

# PostgreSQL URL 형식 변환
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# SQLite인 경우
if DATABASE_URL and DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    # PostgreSQL 등 다른 데이터베이스
    if not DATABASE_URL:
        logger.error("DATABASE_URL is not set! Using SQLite fallback.")
        DATABASE_URL = settings.database_url_sqlite
        engine = create_engine(
            DATABASE_URL, connect_args={"check_same_thread": False}
        )
    else:
        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,
            pool_recycle=300,
            echo=False
        )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """데이터베이스 세션 생성"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}", exc_info=True)
        db.rollback()
        raise
    finally:
        db.close()




