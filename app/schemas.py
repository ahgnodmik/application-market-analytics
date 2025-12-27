from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class FeatureCreate(BaseModel):
    name: str
    description: Optional[str] = None
    feature_type: str  # input, storage, query, notification, media
    difficulty_score: Optional[float] = None


class FeatureResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    feature_type: str
    difficulty_score: float

    class Config:
        from_attributes = True


class AppCreate(BaseModel):
    name: str
    category: Optional[str] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    price_model: Optional[str] = None
    last_update: Optional[datetime] = None
    description: Optional[str] = None


class AppUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    price_model: Optional[str] = None
    last_update: Optional[datetime] = None
    description: Optional[str] = None


class AppResponse(BaseModel):
    id: int
    name: str
    category: Optional[str]
    rating: Optional[float]
    review_count: Optional[int]
    price_model: Optional[str]
    last_update: Optional[datetime]
    description: Optional[str]
    difficulty_score: float
    marketability_score: float
    created_at: datetime
    features: List[FeatureResponse] = []

    class Config:
        from_attributes = True


class AppTypeResponse(BaseModel):
    id: int
    name: str
    core_features: List[str]
    mvp_screens: Optional[int]
    build_time: Optional[str]
    notes: Optional[str]
    avg_difficulty: Optional[float]
    avg_marketability: Optional[float]
    app_count: int

    class Config:
        from_attributes = True


class FilterConfig(BaseModel):
    min_marketability: float = 6.0
    max_difficulty: float = 1.0
    max_features: int = 5




