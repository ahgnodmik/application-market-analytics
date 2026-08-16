"""
데이터 파이프라인 (기획서 16.3)
scrape → normalize → store → analyze → recommend
단계별 함수 분리로 디버깅/재처리 가능
"""
import logging
from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.models import App, Feature, AppType
from app.services.play_store_scraper import fetch_top_apps, fetch_app_details
from app.services.marketability_scorer import calculate_marketability_score
from app.services.difficulty_scorer import calculate_app_difficulty, calculate_feature_difficulty
from app.services.type_grouper import (
    group_apps_by_type,
    generate_type_name,
    estimate_build_time,
    estimate_mvp_screens
)

logger = logging.getLogger(__name__)


async def scrape_playstore_apps(
    category: str = "top_free",
    limit: int = 100,
    play_category: Optional[str] = None
) -> List[Dict]:
    """
    Step 1: Play Store에서 앱 데이터 스크랩
    
    Returns:
        원본 앱 데이터 리스트
    """
    logger.info(f"Scraping Play Store apps: category={category}, limit={limit}, play_category={play_category}")
    from app.services.play_store_scraper import fetch_top_apps
    apps = await fetch_top_apps(category=category, limit=limit, play_category=play_category)
    logger.info(f"Scraped {len(apps)} apps")
    return apps


def normalize_app_data(raw_apps: List[Dict]) -> List[Dict]:
    """
    Step 2: 원본 데이터 정규화
    
    Args:
        raw_apps: Play Store에서 가져온 원본 데이터
    
    Returns:
        정규화된 앱 데이터 리스트
    """
    logger.info(f"Normalizing {len(raw_apps)} apps")
    normalized = []
    
    for app_data in raw_apps:
        normalized_app = {
            "name": app_data.get("name", "Unknown"),
            "package_name": app_data.get("package_name"),
            "category": app_data.get("category"),
            "rating": app_data.get("rating", 0.0),
            "review_count": app_data.get("review_count", 0),
            "price_model": app_data.get("price_model", "free"),
            "description": app_data.get("description", ""),
            "last_update": app_data.get("last_update"),
        }
        normalized.append(normalized_app)
    
    logger.info(f"Normalized {len(normalized)} apps")
    return normalized


def store_apps(
    normalized_apps: List[Dict],
    db: Session,
    update_existing: bool = True
) -> Dict:
    """
    Step 3: 정규화된 데이터를 데이터베이스에 저장
    
    Args:
        normalized_apps: 정규화된 앱 데이터
        db: 데이터베이스 세션
        update_existing: 기존 앱 업데이트 여부
    
    Returns:
        저장 결과 통계
    """
    logger.info(f"Storing {len(normalized_apps)} apps to database")
    
    saved_count = 0
    updated_count = 0
    skipped_count = 0
    
    for app_data in normalized_apps:
        try:
            package_name = app_data.get("package_name")
            
            if not package_name:
                skipped_count += 1
                continue
            
            # 기존 앱 확인
            existing = db.query(App).filter(App.package_name == package_name).first()
            
            if existing and update_existing:
                # 업데이트
                existing.name = app_data.get("name", existing.name)
                existing.category = app_data.get("category", existing.category)
                existing.rating = app_data.get("rating", existing.rating)
                existing.review_count = app_data.get("review_count", existing.review_count)
                existing.price_model = app_data.get("price_model", existing.price_model)
                existing.description = app_data.get("description", existing.description)
                existing.last_update = app_data.get("last_update")
                
                # 시장성 점수 재계산
                existing.marketability_score = calculate_marketability_score(
                    review_count=existing.review_count or 0,
                    rating=existing.rating or 0.0,
                    last_update=app_data.get("last_update"),
                    price_model=existing.price_model,
                    description=existing.description or ""
                )
                
                # 난이도 점수 재계산 (기능이 없으면 설명 기반 추정)
                if not existing.features or len(existing.features) == 0:
                    from app.services.difficulty_scorer import estimate_difficulty_from_description
                    existing.difficulty_score = estimate_difficulty_from_description(existing.description or "")
                else:
                    # 기능이 있으면 기능 기반 계산
                    feature_scores = [f.difficulty_score or 0.0 for f in existing.features]
                    existing.difficulty_score = calculate_app_difficulty(feature_scores)
                
                db.commit()
                updated_count += 1
                
            elif not existing:
                # 새 앱 생성
                description = app_data.get("description", "")
                
                # 난이도 점수 계산 (기능이 없으면 설명 기반 추정)
                from app.services.difficulty_scorer import estimate_difficulty_from_description
                estimated_difficulty = estimate_difficulty_from_description(description)
                
                db_app = App(
                    name=app_data.get("name", "Unknown"),
                    package_name=package_name,
                    category=app_data.get("category"),
                    rating=app_data.get("rating"),
                    review_count=app_data.get("review_count", 0),
                    price_model=app_data.get("price_model", "free"),
                    description=description,
                    last_update=app_data.get("last_update"),
                    difficulty_score=estimated_difficulty,  # 설명 기반 추정
                    marketability_score=calculate_marketability_score(
                        review_count=app_data.get("review_count", 0),
                        rating=app_data.get("rating", 0.0),
                        last_update=app_data.get("last_update"),
                        price_model=app_data.get("price_model", "free"),
                        description=description
                    )
                )
                
                db.add(db_app)
                db.commit()
                saved_count += 1
            else:
                skipped_count += 1
                
        except Exception as e:
            db.rollback()
            logger.error(f"Error storing app {app_data.get('name')}: {e}")
            skipped_count += 1
            continue
    
    result = {
        "saved": saved_count,
        "updated": updated_count,
        "skipped": skipped_count,
        "total": len(normalized_apps)
    }
    
    logger.info(f"Storage complete: {result}")
    return result


def analyze_apps(
    db: Session,
    min_marketability: float = 6.0,
    max_difficulty: float = 1.0,
    max_features: int = 5
) -> List[AppType]:
    """
    Step 4: 저장된 앱들을 분석하여 앱 타입 도출
    
    Args:
        db: 데이터베이스 세션
        min_marketability: 최소 시장성 점수
        max_difficulty: 최대 난이도
        max_features: 최대 기능 수
    
    Returns:
        분석된 앱 타입 리스트
    """
    logger.info(f"Analyzing apps: marketability>={min_marketability}, difficulty<={max_difficulty}, features<={max_features}")
    
    # 필터링된 앱 조회
    apps = db.query(App).filter(
        App.package_name.isnot(None),
        App.package_name != "",
        App.marketability_score >= min_marketability,
        App.difficulty_score <= max_difficulty
    ).all()
    
    # 기능 수로 추가 필터링
    filtered_apps = [
        app for app in apps
        if len(app.features) <= max_features and len(app.features) > 0
    ]
    
    if not filtered_apps:
        logger.info("No apps match the criteria")
        return []
    
    # 앱 타입 그룹화
    groups = group_apps_by_type(filtered_apps)
    
    # 앱 타입 생성
    app_types = []
    for group_key, group_apps in groups.items():
        if not group_apps:
            continue
        
        sample_app = group_apps[0]
        if not sample_app.features:
            continue
        
        feature_names = [f.name for f in sample_app.features[:max_features]]
        if not feature_names:
            continue
        
        type_name = generate_type_name(feature_names)
        avg_difficulty = sum(app.difficulty_score or 0 for app in group_apps) / len(group_apps)
        avg_marketability = sum(app.marketability_score or 0 for app in group_apps) / len(group_apps)
        mvp_screens = estimate_mvp_screens(len(feature_names))
        build_time = estimate_build_time(len(feature_names), avg_difficulty)
        
        # DB에 저장 또는 업데이트
        db_type = db.query(AppType).filter(AppType.name == type_name).first()
        if db_type:
            db_type.core_features = feature_names
            db_type.mvp_screens = mvp_screens
            db_type.build_time = build_time
            db_type.avg_difficulty = avg_difficulty
            db_type.avg_marketability = avg_marketability
            db_type.app_count = len(group_apps)
        else:
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
    logger.info(f"Analysis complete: {len(app_types)} app types generated")
    return app_types


def recommend_app_types(
    db: Session,
    min_marketability: float = 6.0,
    max_difficulty: float = 1.0,
    max_features: int = 5
) -> List[AppType]:
    """
    Step 5: 분석 결과를 바탕으로 추천 앱 타입 반환
    
    Args:
        db: 데이터베이스 세션
        min_marketability: 최소 시장성 점수
        max_difficulty: 최대 난이도
        max_features: 최대 기능 수
    
    Returns:
        추천 앱 타입 리스트
    """
    logger.info(f"Recommending app types with criteria: marketability>={min_marketability}, difficulty<={max_difficulty}")
    
    # 분석 실행 (이미 분석된 타입이 있으면 재사용, 없으면 새로 분석)
    app_types = analyze_apps(db, min_marketability, max_difficulty, max_features)
    
    # 필터링된 결과 반환
    return app_types


async def run_full_pipeline(
    db: Session,
    category: str = "top_free",
    limit: int = 100,
    play_category: Optional[str] = None,
    analyze: bool = True,
    recommend: bool = True
) -> Dict:
    """
    전체 파이프라인 실행 (scrape → normalize → store → analyze → recommend)
    
    Args:
        db: 데이터베이스 세션
        category: 순위 카테고리
        limit: 가져올 앱 수
        play_category: Play Store 카테고리
        analyze: 분석 실행 여부
        recommend: 추천 실행 여부
    
    Returns:
        파이프라인 실행 결과
    """
    logger.info("=" * 60)
    logger.info("Starting full pipeline execution")
    logger.info(f"Category: {category}, Limit: {limit}, Play Category: {play_category}")
    logger.info("=" * 60)
    
    result = {
        "scrape": None,
        "normalize": None,
        "store": None,
        "analyze": None,
        "recommend": None
    }
    
    try:
        # Step 1: Scrape
        raw_apps = await scrape_playstore_apps(category=category, limit=limit, play_category=play_category)
        result["scrape"] = {"count": len(raw_apps), "success": True}
        
        # Step 2: Normalize
        normalized_apps = normalize_app_data(raw_apps)
        result["normalize"] = {"count": len(normalized_apps), "success": True}
        
        # Step 3: Store
        store_result = store_apps(normalized_apps, db)
        result["store"] = store_result
        
        # Step 4: Analyze (선택사항)
        if analyze:
            app_types = analyze_apps(db)
            result["analyze"] = {"count": len(app_types), "success": True}
        
        # Step 5: Recommend (선택사항)
        if recommend:
            recommendations = recommend_app_types(db)
            result["recommend"] = {"count": len(recommendations), "success": True}
        
        logger.info("Pipeline execution complete")
        logger.info(f"Results: {result}")
        
    except Exception as e:
        logger.error(f"Pipeline error: {e}", exc_info=True)
        result["error"] = str(e)
    
    return result
