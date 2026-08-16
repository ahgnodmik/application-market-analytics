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
import logging

logger = logging.getLogger(__name__)

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
    
    기획서 기준:
    - 시장성 점수 >= 6.0
    - 구현 난이도 <= 1.0
    - 핵심 기능 수 <= 5
    
    조건: 시장성 점수 >= min_marketability, 구현 난이도 <= max_difficulty, 핵심 기능 수 <= max_features
    
    주의: Play Store에서 가져온 앱은 기본적으로 기능(features)이 없으므로,
    추천 기능은 기능이 추가된 앱에 대해서만 작동합니다.
    """
    try:
        # Play Store에서 가져온 앱만 필터링
        apps = db.query(App).filter(
            App.package_name.isnot(None),
            App.package_name != "",
            App.marketability_score >= min_marketability,
            App.difficulty_score <= max_difficulty
        ).all()
        
        # 기능 수로 추가 필터링 (기능이 있는 앱만)
        filtered_apps = [
            app for app in apps 
            if len(app.features) <= max_features and len(app.features) > 0
        ]
        
        if not filtered_apps:
            # 기능이 없는 경우 빈 배열 반환 (에러 아님)
            return []
        
        # 앱 타입 그룹화
        try:
            groups = group_apps_by_type(filtered_apps)
        except Exception as e:
            logger.error(f"Error grouping apps by type: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return []
        
        # 앱 타입 생성
        app_types = []
        try:
            for group_key, group_apps in groups.items():
                if not group_apps:
                    continue
                
                # 첫 번째 앱의 기능들을 사용
                sample_app = group_apps[0]
                if not sample_app.features:
                    continue
                    
                feature_names = [f.name for f in sample_app.features[:max_features]]
                
                if not feature_names:
                    continue
                
                # 타입 이름 생성
                try:
                    type_name = generate_type_name(feature_names)
                except Exception as e:
                    logger.error(f"Error generating type name: {e}")
                    continue
                
                # 통계 계산
                avg_difficulty = sum(app.difficulty_score or 0 for app in group_apps) / len(group_apps)
                avg_marketability = sum(app.marketability_score or 0 for app in group_apps) / len(group_apps)
                
                # MVP 정보 추정
                try:
                    mvp_screens = estimate_mvp_screens(len(feature_names))
                    build_time = estimate_build_time(len(feature_names), avg_difficulty)
                except Exception as e:
                    logger.error(f"Error estimating MVP info: {e}")
                    mvp_screens = len(feature_names) * 2
                    build_time = "2-4주"
                
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
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating app types: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return []
        
        # 응답 생성
        return app_types
        
    except Exception as e:
        logger.error(f"Error in get_recommendations: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return []


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
    Play Store에서 가져온 앱만 포함
    """
    try:
        # Play Store에서 가져온 앱만 조회
        apps = db.query(App).filter(
            App.package_name.isnot(None),
            App.package_name != ""
        ).all()
        
        matrix_data = [
            {
                "id": app.id,
                "name": app.name,
                "difficulty": app.difficulty_score or 0.0,
                "marketability": app.marketability_score or 0.0,
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
    except Exception as e:
        logger.error(f"Error in get_matrix_data: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return {
            "apps": [],
            "total": 0
        }
