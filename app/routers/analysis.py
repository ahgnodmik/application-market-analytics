from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import App, AppType
from app.schemas import AppTypeResponse, FilterConfig
from app.services.type_grouper import (
    group_apps_by_type,
    generate_type_name,
    estimate_build_time,
    estimate_mvp_screens
)

router = APIRouter(prefix="/api/analysis", tags=["analysis"])


@router.get("/recommendations", response_model=List[AppTypeResponse])
def get_recommendations(
    min_marketability: float = 6.0,
    max_difficulty: float = 1.0,
    max_features: int = 5,
    db: Session = Depends(get_db)
):
    """
    필터 조건에 맞는 앱 타입 추천
    조건: 시장성 점수 >= min_marketability, 구현 난이도 <= max_difficulty, 핵심 기능 수 <= max_features
    """
    # 조건에 맞는 앱 필터링
    apps = db.query(App).filter(
        App.marketability_score >= min_marketability,
        App.difficulty_score <= max_difficulty
    ).all()
    
    # 기능 수로 추가 필터링
    filtered_apps = [
        app for app in apps 
        if len(app.features) <= max_features
    ]
    
    if not filtered_apps:
        return []
    
    # 앱 타입 그룹화
    groups = group_apps_by_type(filtered_apps)
    
    # 앱 타입 생성
    app_types = []
    for group_key, group_apps in groups.items():
        if not group_apps:
            continue
        
        # 첫 번째 앱의 기능들을 사용
        sample_app = group_apps[0]
        feature_names = [f.name for f in sample_app.features[:max_features]]
        
        if not feature_names:
            continue
        
        # 타입 이름 생성
        type_name = generate_type_name(feature_names)
        
        # 통계 계산
        avg_difficulty = sum(app.difficulty_score for app in group_apps) / len(group_apps)
        avg_marketability = sum(app.marketability_score for app in group_apps) / len(group_apps)
        
        # MVP 정보 추정
        mvp_screens = estimate_mvp_screens(len(feature_names))
        build_time = estimate_build_time(len(feature_names), avg_difficulty)
        
        # 기존 타입 확인 또는 생성
        db_type = db.query(AppType).filter(AppType.name == type_name).first()
        if db_type:
            # 업데이트
            db_type.core_features = feature_names
            db_type.mvp_screens = mvp_screens
            db_type.build_time = build_time
            db_type.avg_difficulty = avg_difficulty
            db_type.avg_marketability = avg_marketability
            db_type.app_count = len(group_apps)
        else:
            # 생성
            db_type = AppType(
                name=type_name,
                core_features=feature_names,
                mvp_screens=mvp_screens,
                build_time=build_time,
                avg_difficulty=avg_difficulty,
                avg_marketability=avg_marketability,
                app_count=len(group_apps)
            )
            db.add(db_type)
        
        app_types.append(db_type)
    
    db.commit()
    
    # 응답 생성
    return app_types


@router.get("/types", response_model=List[AppTypeResponse])
def list_app_types(db: Session = Depends(get_db)):
    """모든 앱 타입 목록 조회"""
    types = db.query(AppType).all()
    return types


@router.get("/types/{type_id}", response_model=AppTypeResponse)
def get_app_type(type_id: int, db: Session = Depends(get_db)):
    """앱 타입 상세 조회"""
    app_type = db.query(AppType).filter(AppType.id == type_id).first()
    if not app_type:
        raise HTTPException(status_code=404, detail="App type not found")
    return app_type


@router.get("/matrix")
def get_matrix_data(db: Session = Depends(get_db)):
    """
    2축 매트릭스 데이터 (X: 구현 난이도, Y: 시장성 점수)
    """
    apps = db.query(App).all()
    
    matrix_data = [
        {
            "id": app.id,
            "name": app.name,
            "difficulty": app.difficulty_score,
            "marketability": app.marketability_score,
            "category": app.category,
            "rating": app.rating,
            "review_count": app.review_count
        }
        for app in apps
    ]
    
    return {
        "apps": matrix_data,
        "total": len(matrix_data)
    }




