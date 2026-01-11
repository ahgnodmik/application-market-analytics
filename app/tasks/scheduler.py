"""
매주 월요일 GMT+9 기준으로 Play Store 순위를 가져오는 스케줄러
Railway에서 cron job으로 실행되거나 FastAPI startup event에서 체크
"""
import asyncio
import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app.database import SessionLocal
from app.models import App
from app.services.play_store_scraper import fetch_top_apps, should_fetch_this_week
from app.services.marketability_scorer import calculate_marketability_score

logger = logging.getLogger(__name__)


async def check_and_fetch_rankings():
    """
    매주 월요일인지 확인하고, 월요일이면 순위를 가져옴
    Railway cron job 또는 FastAPI startup event에서 호출
    """
    if not should_fetch_this_week():
        current_time = datetime.now(ZoneInfo("Asia/Seoul"))
        weekday_names = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
        logger.info(f"오늘은 {weekday_names[current_time.weekday()]}이므로 순위를 가져오지 않습니다.")
        return None
    
    logger.info("월요일이므로 Play Store 순위를 가져옵니다...")
    db = SessionLocal()
    
    try:
        # Play Store에서 앱 목록 가져오기
        apps_data = await fetch_top_apps(category="top_free", limit=100)
        
        if not apps_data:
            logger.warning("앱 데이터를 가져올 수 없습니다.")
            return None
        
        # 데이터베이스에 저장
        saved_count = 0
        updated_count = 0
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
                        updated_count += 1
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
                saved_count += 1
                
            except Exception as e:
                db.rollback()
                logger.error(f"Error saving app {app_data.get('name')}: {e}")
                skipped_count += 1
                continue
        
        result = {
            "success": True,
            "saved_count": saved_count,
            "updated_count": updated_count,
            "skipped_count": skipped_count,
            "fetched_at": datetime.now(ZoneInfo("Asia/Seoul")).isoformat()
        }
        
        logger.info(f"순위 가져오기 완료: {saved_count}개 저장, {updated_count}개 업데이트")
        return result
        
    except Exception as e:
        logger.error(f"순위 가져오기 실패: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None
    finally:
        db.close()


async def periodic_check():
    """
    주기적으로 확인하는 함수 (백그라운드 태스크용)
    """
    while True:
        await check_and_fetch_rankings()
        # 다음 월요일까지 대기 (대략)
        await asyncio.sleep(3600 * 24)  # 24시간마다 확인
