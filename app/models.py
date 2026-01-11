from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class App(Base):
    __tablename__ = "apps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    package_name = Column(String, unique=True, index=True)  # Google Play Store 패키지 이름 (UNIQUE - 기획서 14.4)
    category = Column(String, index=True)  # INDEX 추가 (기획서 14.4)
    rating = Column(Float)
    review_count = Column(Integer)
    price_model = Column(String)  # free, paid, subscription
    last_update = Column(DateTime)
    description = Column(Text)
    
    # 계산된 점수
    difficulty_score = Column(Float, default=0.0)
    marketability_score = Column(Float, default=0.0)
    
    # 메타데이터
    created_at = Column(DateTime, default=datetime.utcnow)
    
    features = relationship("Feature", back_populates="app", cascade="all, delete-orphan")


class Feature(Base):
    __tablename__ = "features"

    id = Column(Integer, primary_key=True, index=True)
    app_id = Column(Integer, ForeignKey("apps.id"), nullable=False)
    name = Column(String, nullable=False)
    feature_type = Column(String)  # input, storage, query, notification, media
    difficulty_score = Column(Float, default=0.0)
    description = Column(Text, nullable=True)
    
    app = relationship("App", back_populates="features")


class AppType(Base):
    __tablename__ = "app_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)  # INDEX 추가 (기획서 14.4)
    core_features = Column(JSON)
    mvp_screens = Column(Integer)
    build_time = Column(String)
    avg_difficulty = Column(Float)
    avg_marketability = Column(Float)
    app_count = Column(Integer, default=0)
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)


class ScheduledTask(Base):
    """
    스케줄러 작업 상태 관리 (기획서 14.5)
    중복 실행 방지를 위한 작업 테이블
    """
    __tablename__ = "scheduled_tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String, nullable=False, index=True)  # 예: "weekly_fetch_rankings"
    task_date = Column(String, nullable=False)  # YYYY-WW 형식 (예: "2024-01" = 2024년 1주차)
    status = Column(String, default="pending")  # pending, running, completed, failed
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    result_data = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        # 동일 작업-날짜 조합은 유일해야 함 (중복 방지)
        {"sqlite_autoincrement": True},
    )
