"""
Google Play Store 앱 순위 가져오기 라우터
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

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

router = APIRouter(prefix="/api/playstore", tags=["playstore"])


async def fetch_rankings_impl(
    category: str = "top_free",
    limit: int = 100,
    force: bool = False,
    db: Session = None
):
    """
    Google Play Store에서 앱 순위 가져오기
    
    Args:
        category: 카테고리 ("top_free", "top_paid", "top_grossing")
        limit: 가져올 앱 수 (최대 100)
        force: 월요일이 아니어도 강제로 가져오기
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
        apps_data = await fetch_top_apps(category=category, limit=limit)
        
        if not apps_data:
            raise HTTPException(status_code=500, detail="앱 데이터를 가져올 수 없습니다.")
        
        # 데이터베이스에 저장
        saved_apps = []
        skipped_count = 0
        
        for app_data in apps_data:
            # 이미 존재하는 앱인지 확인 (패키지 이름 기준)
            package_name = app_data.get("package_name")
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
            try:
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
            "fetched_at": datetime.now(ZoneInfo("Asia/Seoul")).isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"앱 순위 가져오기 실패: {str(e)}")


@router.get("/last-fetch")
async def get_last_fetch_info(db: Session = Depends(get_db)):
    """
    마지막으로 앱 순위를 가져온 시간 확인
    """
    # 가장 최근에 추가/업데이트된 앱의 시간 확인
    latest_app = db.query(App).order_by(App.id.desc()).first()
    
    if not latest_app:
        return {
            "last_fetch": None,
            "message": "아직 앱 데이터를 가져온 적이 없습니다."
        }
    
    # 다음 월요일 계산 (GMT+9)
    kst = ZoneInfo("Asia/Seoul")
    now = datetime.now(kst)
    days_until_monday = (7 - now.weekday()) % 7
    if days_until_monday == 0 and now.hour < 9:  # 월요일 오전 9시 전
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
