from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class App(Base):
    __tablename__ = "apps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    category = Column(String)
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
    description = Column(Text)
    feature_type = Column(String)  # input, storage, query, notification, media
    difficulty_score = Column(Float, default=0.0)  # 0~2
    
    app = relationship("App", back_populates="features")


class AppType(Base):
    __tablename__ = "app_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    core_features = Column(JSON)  # 리스트로 저장
    mvp_screens = Column(Integer)
    build_time = Column(String)
    notes = Column(Text)
    
    # 통계
    avg_difficulty = Column(Float)
    avg_marketability = Column(Float)
    app_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)




