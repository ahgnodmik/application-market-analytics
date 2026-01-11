"""
Google Play Store 앱 순위 가져오기 라우터
카테고리별 순위 수집 및 GPT 분석 기능 포함
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from pydantic import BaseModel

from app.database import get_db
from app.models import App
from app.schemas import AppCreate, AppResponse
from app.services.play_store_scraper import (
    fetch_top_apps,
    should_fetch_this_week,
    fetch_app_details
)
from app.services.marketability_scorer import calculate_marketability_score
from app.services.difficulty_scorer import calculate_app_difficulty
from app.services.category_analyzer import (
    analyze_category_with_gpt,
    analyze_multiple_categories_with_gpt
)
from app.services.play_store_scraper_real import get_category_list

router = APIRouter(prefix="/api/playstore", tags=["playstore"])


class CategoryAnalysisRequest(BaseModel):
    categories: List[str]  # 분석할 카테고리 목록
    limit_per_category: int = 50  # 카테고리당 가져올 앱 수
    ranking_type: str = "top_free"  # top_free, top_paid, top_grossing


async def fetch_rankings_impl(
    category: str = "top_free",
    limit: int = 100,
    force: bool = False,
    play_category: Optional[str] = None,
    db: Session = None
):
    """
    Google Play Store에서 앱 순위 가져오기
    
    Args:
        category: 순위 타입 ("top_free", "top_paid", "top_grossing")
        limit: 가져올 앱 수 (최대 100)
        force: 월요일이 아니어도 강제로 가져오기
        play_category: Play Store 카테고리 (예: "APPLICATION_SOCIAL", "GAME" 등)
    """
    # 월요일인지 확인 (GMT+9 기준)
    if not force and not should_fetch_this_week():
        current_time = datetime.now(ZoneInfo("Asia/Seoul"))
        weekday_names = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
        raise HTTPException(
            status_code=400,
            detail=f"앱 순위는 매주 월요일(GMT+9)에만 가져올 수 있습니다. 현재는 {weekday_names[current_time.weekday()]}입니다."
        )
    
    try:
        # Play Store에서 앱 목록 가져오기
        apps_data = await fetch_top_apps(category=category, limit=limit, play_category=play_category)
        
        if not apps_data:
            raise HTTPException(status_code=500, detail="앱 데이터를 가져올 수 없습니다.")
        
        # 데이터베이스에 저장
        saved_apps = []
        skipped_count = 0
        
        for app_data in apps_data:
            try:
                package_name = app_data.get("package_name")
                
                # 이미 존재하는 앱인지 확인 (패키지 이름 기준)
                if package_name:
                    existing = db.query(App).filter(App.package_name == package_name).first()
                    if existing:
                        # 기존 앱 업데이트
                        existing.name = app_data.get("name", existing.name)
                        existing.category = app_data.get("category", existing.category)
                        existing.rating = app_data.get("rating", existing.rating)
                        existing.review_count = app_data.get("review_count", existing.review_count)
                        existing.price_model = app_data.get("price_model", existing.price_model)
                        existing.description = app_data.get("description", existing.description)
                        
                        # 시장성 점수 재계산
                        existing.marketability_score = calculate_marketability_score(
                            review_count=existing.review_count or 0,
                            rating=existing.rating or 0.0,
                            last_update=app_data.get("last_update"),
                            price_model=existing.price_model,
                            description=existing.description or ""
                        )
                        
                        db.commit()
                        db.refresh(existing)
                        saved_apps.append(existing)
                        continue
                
                # 새 앱 생성
                db_app = App(
                    name=app_data.get("name", "Unknown"),
                    package_name=package_name,
                    category=app_data.get("category"),
                    rating=app_data.get("rating"),
                    review_count=app_data.get("review_count", 0),
                    price_model=app_data.get("price_model", "free"),
                    description=app_data.get("description", ""),
                    difficulty_score=0.0,  # 나중에 기능 분석 시 계산
                    marketability_score=calculate_marketability_score(
                        review_count=app_data.get("review_count", 0),
                        rating=app_data.get("rating", 0.0),
                        last_update=app_data.get("last_update"),
                        price_model=app_data.get("price_model", "free"),
                        description=app_data.get("description", "")
                    )
                )
                
                db.add(db_app)
                db.commit()
                db.refresh(db_app)
                saved_apps.append(db_app)
                
            except Exception as e:
                db.rollback()
                print(f"Error saving app {app_data.get('name')}: {e}")
                skipped_count += 1
                continue
        
        return {
            "success": True,
            "message": f"{len(saved_apps)}개 앱 가져오기 완료",
            "saved_count": len(saved_apps),
            "skipped_count": skipped_count,
            "category": category,
            "play_category": play_category,
            "fetched_at": datetime.now(ZoneInfo("Asia/Seoul")).isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"앱 순위 가져오기 실패: {str(e)}")


@router.post("/fetch-rankings")
async def fetch_rankings(
    category: str = "top_free",
    limit: int = 100,
    play_category: Optional[str] = None,
    force: bool = False,
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """
    Google Play Store에서 앱 순위 가져오기
    
    Args:
        category: 순위 타입 ("top_free", "top_paid", "top_grossing")
        limit: 가져올 앱 수 (최대 100)
        play_category: Play Store 카테고리 (예: "APPLICATION_SOCIAL", "GAME" 등)
        force: 월요일이 아니어도 강제로 가져오기
    """
    return await fetch_rankings_impl(category=category, limit=limit, force=force, play_category=play_category, db=db)


@router.get("/categories")
async def get_categories():
    """
    사용 가능한 Play Store 카테고리 목록 반환
    """
    try:
        categories = get_category_list()
        return {
            "success": True,
            "categories": categories,
            "total": len(categories)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "categories": []
        }


@router.post("/fetch-by-category")
async def fetch_by_category(
    play_category: str,
    category: str = "top_free",
    limit: int = 100,
    force: bool = False,
    db: Session = Depends(get_db)
):
    """
    특정 카테고리별 앱 순위 가져오기
    
    Args:
        play_category: Play Store 카테고리 (예: "APPLICATION_SOCIAL", "GAME" 등)
        category: 순위 타입 ("top_free", "top_paid", "top_grossing")
        limit: 가져올 앱 수
        force: 월요일이 아니어도 강제로 가져오기
    """
    return await fetch_rankings_impl(
        category=category,
        limit=limit,
        force=force,
        play_category=play_category,
        db=db
    )


@router.post("/analyze-category")
async def analyze_category(
    play_category: str,
    category: str = "top_free",
    limit: int = 50,
    force: bool = False,
    db: Session = Depends(get_db)
):
    """
    특정 카테고리의 앱 목록을 GPT로 분석
    
    Args:
        play_category: Play Store 카테고리
        category: 순위 타입
        limit: 분석할 앱 수
        force: 월요일이 아니어도 강제로 가져오기
    """
    try:
        # 앱 데이터 가져오기 (DB 저장 없이 분석만)
        apps_data = await fetch_top_apps(category=category, limit=limit, play_category=play_category)
        
        if not apps_data:
            raise HTTPException(status_code=500, detail="앱 데이터를 가져올 수 없습니다.")
        
        # GPT로 분석
        analysis_result = await analyze_category_with_gpt(
            apps_data=apps_data,
            category_name=play_category,
            limit=limit
        )
        
        if not analysis_result.get("success"):
            raise HTTPException(status_code=500, detail=analysis_result.get("error", "분석 실패"))
        
        return analysis_result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"카테고리 분석 실패: {str(e)}")


@router.post("/analyze-multiple-categories")
async def analyze_multiple_categories(
    request: CategoryAnalysisRequest,
    db: Session = Depends(get_db)
):
    """
    여러 카테고리별 앱 목록을 GPT로 비교 분석
    
    Args:
        request: 분석 요청 (카테고리 목록, 제한 등)
    """
    try:
        # 각 카테고리별로 앱 데이터 가져오기
        category_apps_map = {}
        
        for play_category in request.categories:
            apps_data = await fetch_top_apps(
                category=request.ranking_type,
                limit=request.limit_per_category,
                play_category=play_category
            )
            if apps_data:
                category_apps_map[play_category] = apps_data
        
        if not category_apps_map:
            raise HTTPException(status_code=500, detail="카테고리 데이터를 가져올 수 없습니다.")
        
        # GPT로 비교 분석
        analysis_result = await analyze_multiple_categories_with_gpt(
            category_apps_map=category_apps_map,
            limit_per_category=request.limit_per_category
        )
        
        if not analysis_result.get("success"):
            raise HTTPException(status_code=500, detail=analysis_result.get("error", "분석 실패"))
        
        return analysis_result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"다중 카테고리 분석 실패: {str(e)}")


@router.get("/last-fetch")
async def get_last_fetch_info(db: Session = Depends(get_db)):
    """
    마지막으로 앱 순위를 가져온 시간 확인
    """
    latest_app = db.query(App).order_by(App.id.desc()).first()
    
    if not latest_app:
        return {
            "last_fetch": None,
            "message": "아직 앱 데이터를 가져온 적이 없습니다."
        }
    
    kst = ZoneInfo("Asia/Seoul")
    now = datetime.now(kst)
    days_until_monday = (7 - now.weekday()) % 7
    if days_until_monday == 0 and now.hour < 9:
        next_monday = now.replace(hour=9, minute=0, second=0, microsecond=0)
    else:
        if days_until_monday == 0:
            days_until_monday = 7
        next_monday = (now.replace(hour=9, minute=0, second=0, microsecond=0) + 
                      timedelta(days=days_until_monday))
    
    return {
        "last_fetch": latest_app.created_at.isoformat() if hasattr(latest_app, 'created_at') else None,
        "next_scheduled_fetch": next_monday.isoformat(),
        "can_fetch_now": should_fetch_this_week()
    }


@router.get("/status")
async def get_fetch_status():
    """
    현재 앱 순위를 가져올 수 있는지 상태 확인
    """
    current_time = datetime.now(ZoneInfo("Asia/Seoul"))
    weekday_names = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    
    return {
        "current_time": current_time.isoformat(),
        "current_weekday": weekday_names[current_time.weekday()],
        "can_fetch": should_fetch_this_week(),
        "timezone": "GMT+9 (Asia/Seoul)"
    }
