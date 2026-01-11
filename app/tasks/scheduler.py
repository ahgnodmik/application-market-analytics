"""
매주 월요일 GMT+9 기준으로 Play Store 순위를 가져오는 스케줄러
Railway에서 cron job으로 실행되거나 FastAPI startup event에서 체크

기획서 14.5: 중복 실행 방지 강화 (DB 락/작업 테이블 사용)
"""
import asyncio
import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from sqlalchemy import and_

from app.database import SessionLocal
from app.models import App, ScheduledTask
from app.services.play_store_scraper import fetch_top_apps
from app.services.marketability_scorer import calculate_marketability_score

logger = logging.getLogger(__name__)


def get_week_key() -> str:
    """현재 주차 키 생성 (YYYY-WW 형식)"""
    now = datetime.now(ZoneInfo("Asia/Seoul"))
    year, week, _ = now.isocalendar()
    return f"{year}-{week:02d}"


def is_task_running_or_completed(db, task_name: str, week_key: str) -> bool:
    """
    작업이 실행 중이거나 완료되었는지 확인 (기획서 14.5)
    
    Returns:
        True: 실행 중이거나 완료됨 (중복 실행 방지)
        False: 실행 가능
    """
    task = db.query(ScheduledTask).filter(
        and_(
            ScheduledTask.task_name == task_name,
            ScheduledTask.task_date == week_key
        )
    ).first()
    
    if task:
        if task.status == "completed":
            logger.info(f"Task {task_name} for {week_key} already completed")
            return True
        elif task.status == "running":
            logger.warning(f"Task {task_name} for {week_key} is already running")
            return True
    
    return False


def create_task_record(db, task_name: str, week_key: str) -> ScheduledTask:
    """작업 레코드 생성"""
    task = ScheduledTask(
        task_name=task_name,
        task_date=week_key,
        status="running",
        started_at=datetime.utcnow()
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task_record(db, task: ScheduledTask, status: str, result_data: dict = None, error: str = None):
    """작업 레코드 업데이트"""
    task.status = status
    task.completed_at = datetime.utcnow()
    if result_data:
        task.result_data = result_data
    if error:
        task.error_message = error
    db.commit()


def should_fetch_this_week() -> bool:
    """매주 월요일인지 확인"""
    now = datetime.now(ZoneInfo("Asia/Seoul"))
    return now.weekday() == 0  # 월요일 = 0


async def check_and_fetch_rankings(force: bool = False):
    """
    매주 월요일인지 확인하고, 월요일이면 순위를 가져옴
    기획서 14.5: 중복 실행 방지 강화
    
    Args:
        force: 강제 실행 (중복 체크 무시)
    
    Railway cron job 또는 FastAPI startup event에서 호출
    """
    task_name = "weekly_fetch_rankings"
    week_key = get_week_key()
    db = SessionLocal()
    
    try:
        # 중복 실행 방지 (기획서 14.5)
        if not force and is_task_running_or_completed(db, task_name, week_key):
            logger.info(f"Skipping task {task_name} for {week_key} (already completed/running)")
            return None
        
        # 월요일 체크
        if not force and not should_fetch_this_week():
            current_time = datetime.now(ZoneInfo("Asia/Seoul"))
            weekday_names = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
            logger.info(f"오늘은 {weekday_names[current_time.weekday()]}이므로 순위를 가져오지 않습니다.")
            return None
        
        # 작업 레코드 생성
        task = create_task_record(db, task_name, week_key)
        logger.info(f"Starting task {task_name} for {week_key} (task_id: {task.id})")
        
        # Play Store에서 앱 목록 가져오기
        apps_data = await fetch_top_apps(category="top_free", limit=100)
        
        if not apps_data:
            logger.warning("앱 데이터를 가져올 수 없습니다.")
            update_task_record(db, task, "failed", error="No app data fetched")
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
        
        # 작업 완료 기록
        update_task_record(db, task, "completed", result_data=result)
        
        logger.info(f"순위 가져오기 완료: {saved_count}개 저장, {updated_count}개 업데이트")
        return result
        
    except Exception as e:
        logger.error(f"순위 가져오기 실패: {e}")
        import traceback
        logger.error(traceback.format_exc())
        
        # 작업 실패 기록
        if 'task' in locals():
            update_task_record(db, task, "failed", error=str(e))
        
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
