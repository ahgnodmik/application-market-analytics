from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import App, Feature
from app.schemas import AppCreate, AppUpdate, AppResponse, FeatureCreate, FeatureResponse
from app.services.difficulty_scorer import calculate_feature_difficulty, calculate_app_difficulty
from app.services.marketability_scorer import calculate_marketability_score, parse_date

router = APIRouter(prefix="/api/apps", tags=["apps"])


@router.post("/", response_model=AppResponse)
def create_app(app: AppCreate, db: Session = Depends(get_db)):
    """앱 생성"""
    db_app = App(**app.dict())
    
    # 시장성 점수 계산
    db_app.marketability_score = calculate_marketability_score(
        review_count=app.review_count or 0,
        rating=app.rating or 0.0,
        last_update=app.last_update.isoformat() if app.last_update else None,
        price_model=app.price_model,
        description=app.description or ""
    )
    
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app


@router.get("/", response_model=List[AppResponse])
def list_apps(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """앱 목록 조회"""
    apps = db.query(App).offset(skip).limit(limit).all()
    return apps


@router.get("/{app_id}", response_model=AppResponse)
def get_app(app_id: int, db: Session = Depends(get_db)):
    """앱 상세 조회"""
    app = db.query(App).filter(App.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    return app


@router.put("/{app_id}", response_model=AppResponse)
def update_app(app_id: int, app_update: AppUpdate, db: Session = Depends(get_db)):
    """앱 수정"""
    db_app = db.query(App).filter(App.id == app_id).first()
    if not db_app:
        raise HTTPException(status_code=404, detail="App not found")
    
    update_data = app_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_app, key, value)
    
    # 시장성 점수 재계산
    db_app.marketability_score = calculate_marketability_score(
        review_count=db_app.review_count or 0,
        rating=db_app.rating or 0.0,
        last_update=db_app.last_update.isoformat() if db_app.last_update else None,
        price_model=db_app.price_model,
        description=db_app.description or ""
    )
    
    db.commit()
    db.refresh(db_app)
    return db_app


@router.delete("/{app_id}")
def delete_app(app_id: int, db: Session = Depends(get_db)):
    """앱 삭제"""
    app = db.query(App).filter(App.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    
    db.delete(app)
    db.commit()
    return {"message": "App deleted successfully"}


@router.post("/{app_id}/features", response_model=FeatureResponse)
def add_feature(app_id: int, feature: FeatureCreate, db: Session = Depends(get_db)):
    """앱에 기능 추가"""
    app = db.query(App).filter(App.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    
    # 난이도 점수 계산 (제공되지 않은 경우)
    difficulty = feature.difficulty_score
    if difficulty is None:
        difficulty = calculate_feature_difficulty(
            feature_type=feature.feature_type,
            description=feature.description or ""
        )
    
    db_feature = Feature(
        app_id=app_id,
        name=feature.name,
        description=feature.description,
        feature_type=feature.feature_type,
        difficulty_score=difficulty
    )
    
    db.add(db_feature)
    db.commit()
    
    # 앱 난이도 점수 재계산
    feature_scores = [f.difficulty_score for f in app.features]
    feature_scores.append(difficulty)
    app.difficulty_score = calculate_app_difficulty(feature_scores)
    
    db.commit()
    db.refresh(db_feature)
    return db_feature


@router.get("/{app_id}/features", response_model=List[FeatureResponse])
def list_features(app_id: int, db: Session = Depends(get_db)):
    """앱의 기능 목록 조회"""
    features = db.query(Feature).filter(Feature.app_id == app_id).all()
    return features


@router.delete("/{app_id}/features/{feature_id}")
def delete_feature(app_id: int, feature_id: int, db: Session = Depends(get_db)):
    """기능 삭제"""
    feature = db.query(Feature).filter(
        Feature.id == feature_id,
        Feature.app_id == app_id
    ).first()
    
    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")
    
    app = db.query(App).filter(App.id == app_id).first()
    db.delete(feature)
    db.commit()
    
    # 앱 난이도 점수 재계산
    feature_scores = [f.difficulty_score for f in app.features]
    app.difficulty_score = calculate_app_difficulty(feature_scores) if feature_scores else 0.0
    db.commit()
    
    return {"message": "Feature deleted successfully"}




