"""
Google Play Store 앱 순위 가져오기 라우터
카테고리별 순위 수집 및 GPT 분석 기능 포함
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Body
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
    fetch_app_details
)
from app.tasks.scheduler import should_fetch_this_week
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


class SingleCategoryAnalysisRequest(BaseModel):
    play_category: str  # Play Store 카테고리
    category: Optional[str] = "top_free"  # 순위 타입 (하위 호환성을 위해 Optional)
    ranking_type: Optional[str] = None  # 순위 타입 (프론트엔드에서 사용)
    limit: int = 50  # 분석할 앱 수
    force: bool = False  # 강제 실행


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
    import logging
    logger = logging.getLogger(__name__)
    
    # 월요일인지 확인 (GMT+9 기준)
    if not force and not should_fetch_this_week():
        current_time = datetime.now(ZoneInfo("Asia/Seoul"))
        weekday_names = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
        raise HTTPException(
            status_code=400,
            detail=f"앱 순위는 매주 월요일(GMT+9)에만 가져올 수 있습니다. 현재는 {weekday_names[current_time.weekday()]}입니다."
        )
    
    try:
        # Play Store에서 앱 목록 가져오기 (더 많은 앱을 가져와서 랜덤 선택)
        # 랜덤 선택을 위해 충분한 수를 가져옴 (최소 50개 이상)
        fetch_limit = max(limit * 5, 50)  # 최소 50개 이상 가져오기 (YouTube/Instagram 제외 대비)
        logger.info(f"Fetching {fetch_limit} apps from Play Store (category: {play_category})")
        apps_data = await fetch_top_apps(category=category, limit=fetch_limit, play_category=play_category)
        
        if not apps_data:
            raise HTTPException(status_code=500, detail="앱 데이터를 가져올 수 없습니다.")
        
        # 샘플 데이터인지 확인 (YouTube, Instagram만 있는 경우)
        app_names = [app.get("name", "") for app in apps_data]
        unique_names = set(app_names)
        
        # 샘플 데이터 감지: YouTube/Instagram만 있거나, 고유 앱이 2개 이하인 경우
        is_sample_data = (
            len(unique_names) <= 2 and 
            ("YouTube" in unique_names or "Instagram" in unique_names)
        )
        
        if is_sample_data:
            logger.warning(f"Sample data detected! Only {len(unique_names)} unique apps: {unique_names}")
            logger.warning(f"Attempting to fetch real Play Store data with category: {play_category}")
            
            # 실제 Play Store에서 다시 시도 (더 많은 앱 수집)
            try:
                # 카테고리별로 더 많은 앱 가져오기
                real_apps = await fetch_top_apps(
                    category=category, 
                    limit=50,  # 충분한 수를 가져와서 랜덤 선택
                    play_category=play_category
                )
                
                if real_apps:
                    real_names = set([a.get("name", "") for a in real_apps])
                    if len(real_names) > 2 and not ("YouTube" in real_names and "Instagram" in real_names and len(real_names) == 2):
                        logger.info(f"Successfully fetched {len(real_apps)} real apps with {len(real_names)} unique names")
                        apps_data = real_apps
                    else:
                        logger.warning(f"Still getting limited apps: {real_names}")
                else:
                    logger.error("Failed to fetch real apps")
            except Exception as e:
                logger.error(f"Error fetching real apps: {e}", exc_info=True)
        
        # 데이터베이스에 저장
        saved_apps = []
        updated_apps = []
        skipped_count = 0
        
        # YouTube와 Instagram 제외 필터
        excluded_apps = {
            "com.google.android.youtube",  # YouTube
            "com.instagram.android",  # Instagram
            "youtube",
            "instagram"
        }
        
        # 중복 제거 및 제외 앱 필터링
        logger.info(f"Starting filtering: {len(apps_data)} apps received")
        unique_apps = {}
        excluded_count = 0
        for app in apps_data:
            package_name = app.get("package_name", "").lower()
            app_name = app.get("name", "").lower()
            
            # YouTube/Instagram 제외
            if any(excluded in package_name or excluded in app_name for excluded in excluded_apps):
                excluded_count += 1
                continue
            
            # 중복 제거
            if package_name and package_name not in unique_apps:
                unique_apps[package_name] = app
        
        apps_data_unique = list(unique_apps.values())
        logger.info(f"After filtering: {len(apps_data_unique)} unique apps (excluded: {excluded_count})")
        
        # 필터링 후 앱이 없으면 더 많은 앱을 가져와서 재시도
        if len(apps_data_unique) == 0:
            logger.warning(f"No apps remaining after filtering! Original: {len(apps_data)}, Excluded: {excluded_count}")
            logger.info(f"Attempting to fetch more apps (limit: {fetch_limit * 2}) to find non-excluded apps...")
            
            try:
                # 더 많은 앱을 가져오기 (2배)
                retry_apps_data = await fetch_top_apps(
                    category=category, 
                    limit=fetch_limit * 2, 
                    play_category=play_category
                )
                
                if retry_apps_data and len(retry_apps_data) > len(apps_data):
                    logger.info(f"Retry fetched {len(retry_apps_data)} apps")
                    # 다시 필터링
                    unique_apps = {}
                    excluded_count = 0
                    for app in retry_apps_data:
                        package_name = app.get("package_name", "").lower()
                        app_name = app.get("name", "").lower()
                        
                        if any(excluded in package_name or excluded in app_name for excluded in excluded_apps):
                            excluded_count += 1
                            continue
                        
                        if package_name and package_name not in unique_apps:
                            unique_apps[package_name] = app
                    
                    apps_data_unique = list(unique_apps.values())
                    logger.info(f"After retry filtering: {len(apps_data_unique)} unique apps (excluded: {excluded_count})")
                    
                    # 여전히 없으면 카테고리 없이 전체 앱 목록 시도
                    if len(apps_data_unique) == 0:
                        logger.warning("Still no apps after retry, trying without category filter...")
                        all_apps_data = await fetch_top_apps(
                            category=category,
                            limit=50,
                            play_category=None  # 카테고리 없이 전체 앱 목록
                        )
                        
                        if all_apps_data:
                            unique_apps = {}
                            excluded_count = 0
                            for app in all_apps_data:
                                package_name = app.get("package_name", "").lower()
                                app_name = app.get("name", "").lower()
                                
                                if any(excluded in package_name or excluded in app_name for excluded in excluded_apps):
                                    excluded_count += 1
                                    continue
                                
                                if package_name and package_name not in unique_apps:
                                    unique_apps[package_name] = app
                            
                            apps_data_unique = list(unique_apps.values())
                            logger.info(f"After fetching all apps: {len(apps_data_unique)} unique apps")
                
            except Exception as e:
                logger.error(f"Error during retry: {e}", exc_info=True)
        
        # 최종 확인: 여전히 앱이 없으면 에러
        if len(apps_data_unique) == 0:
            logger.error(f"CRITICAL: No apps remaining after all retry attempts! Original: {len(apps_data)}, Excluded: {excluded_count}")
            raise HTTPException(
                status_code=500, 
                detail=f"필터링 후 수집할 앱이 없습니다. 원본 앱 수: {len(apps_data)}, 제외된 앱: {excluded_count}. Play Store에서 더 많은 앱을 가져오려고 시도했지만 실패했습니다."
            )
        
        # 난이도 점수 계산 및 필터링
        from app.services.difficulty_scorer import estimate_difficulty_from_description
        
        apps_with_difficulty = []
        for app in apps_data_unique:
            description = app.get("description", "")
            difficulty = estimate_difficulty_from_description(description)
            app["estimated_difficulty"] = difficulty
            apps_with_difficulty.append(app)
        
        logger.info(f"Calculated difficulty for {len(apps_with_difficulty)} apps")
        
        # 난이도 기준을 점진적으로 완화하며 앱 선택
        apps_to_process = []
        
        # 1단계: 난이도 1.0 이하 앱 (최우선)
        low_difficulty_apps = [app for app in apps_with_difficulty if app.get("estimated_difficulty", 2.0) <= 1.0]
        logger.info(f"Step 1: Found {len(low_difficulty_apps)} apps with difficulty <= 1.0")
        
        if len(low_difficulty_apps) >= 5:
            import random
            random.shuffle(low_difficulty_apps)
            apps_to_process = low_difficulty_apps[:5]
            logger.info(f"Selected 5 apps from low difficulty pool")
        elif len(low_difficulty_apps) > 0:
            # 난이도 1.0 이하 앱이 있으면 일단 사용
            apps_to_process = low_difficulty_apps.copy()
            logger.info(f"Selected {len(apps_to_process)} apps from low difficulty pool, need more")
        
        # 2단계: 난이도 1.5 이하로 확대 (1단계에서 부족한 경우)
        if len(apps_to_process) < 5:
            medium_difficulty_apps = [
                app for app in apps_with_difficulty 
                if app.get("estimated_difficulty", 2.0) <= 1.5 
                and app not in apps_to_process
            ]
            logger.info(f"Step 2: Found {len(medium_difficulty_apps)} apps with difficulty <= 1.5")
            needed = 5 - len(apps_to_process)
            if len(medium_difficulty_apps) >= needed:
                import random
                random.shuffle(medium_difficulty_apps)
                apps_to_process.extend(medium_difficulty_apps[:needed])
                logger.info(f"Added {needed} apps from medium difficulty pool")
            elif len(medium_difficulty_apps) > 0:
                apps_to_process.extend(medium_difficulty_apps)
                logger.info(f"Added {len(medium_difficulty_apps)} apps from medium difficulty pool")
        
        # 3단계: 난이도 순으로 정렬하여 낮은 것부터 선택 (여전히 부족한 경우)
        if len(apps_to_process) < 5:
            remaining_apps = [
                app for app in apps_with_difficulty 
                if app not in apps_to_process
            ]
            logger.info(f"Step 3: Found {len(remaining_apps)} remaining apps")
            # 난이도 순으로 정렬 (낮은 것부터)
            remaining_apps.sort(key=lambda x: x.get("estimated_difficulty", 2.0))
            needed = 5 - len(apps_to_process)
            apps_to_process.extend(remaining_apps[:needed])
            logger.info(f"Added {min(needed, len(remaining_apps))} apps from remaining pool")
        
        # 최종 확인: 여전히 앱이 없으면 모든 앱 중에서 난이도가 낮은 순으로 선택
        if len(apps_to_process) == 0:
            logger.warning("No apps found after filtering, selecting lowest difficulty apps from all available")
            apps_with_difficulty.sort(key=lambda x: x.get("estimated_difficulty", 2.0))
            apps_to_process = apps_with_difficulty[:min(5, len(apps_with_difficulty))]
            logger.info(f"Final fallback: Selected {len(apps_to_process)} apps")
        
        # 최종적으로 5개로 제한
        apps_to_process = apps_to_process[:5]
        logger.info(f"Final selection: {len(apps_to_process)} apps to process")
        
        if len(apps_to_process) == 0:
            logger.error("CRITICAL: No apps to process after all filtering steps!")
            raise HTTPException(
                status_code=500,
                detail=f"모든 필터링 단계를 거친 후에도 수집할 앱이 없습니다. 원본 앱 수: {len(apps_data)}, 필터링 후: {len(apps_data_unique)}"
            )
        
        for app_data in apps_to_process:
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
                        updated_apps.append(existing)
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
        
        # 저장/업데이트된 모든 앱 목록
        all_processed_apps = saved_apps + updated_apps
        
        # 응답 형식 변환
        from app.schemas import AppResponse
        apps_response = [
            {
                "id": app.id,
                "name": app.name,
                "package_name": app.package_name,
                "category": app.category,
                "rating": app.rating,
                "review_count": app.review_count,
                "price_model": app.price_model,
                "description": app.description,
                "difficulty_score": app.difficulty_score,
                "marketability_score": app.marketability_score,
                "created_at": app.created_at.isoformat() if app.created_at else None
            }
            for app in all_processed_apps
        ]
        
        return {
            "success": True,
            "message": f"{len(saved_apps)}개 새 앱 저장, {len(updated_apps)}개 앱 업데이트 완료",
            "saved_count": len(saved_apps),
            "updated_count": len(updated_apps),
            "total_count": len(all_processed_apps),
            "skipped_count": skipped_count,
            "category": category,
            "play_category": play_category,
            "apps": apps_response,  # 실제 저장/업데이트된 앱 목록
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
    request: SingleCategoryAnalysisRequest,
    db: Session = Depends(get_db)
):
    """
    특정 카테고리의 앱 목록을 GPT로 분석
    
    Args:
        request: 분석 요청 (play_category, category/ranking_type, limit, force)
    """
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        play_category = request.play_category
        # 프론트엔드에서 ranking_type을 보내면 그것을 사용, 아니면 category 사용
        category = request.ranking_type or request.category or "top_free"
        limit = request.limit
        force = request.force
        
        logger.info(f"Analyzing category: {play_category}, ranking_type: {category}, limit: {limit}")
        
        # 앱 데이터 가져오기 (DB 저장 없이 분석만)
        try:
            logger.info(f"Fetching apps: category={category}, play_category={play_category}, limit={limit}")
            apps_data = await fetch_top_apps(category=category, limit=limit, play_category=play_category)
            logger.info(f"Fetched {len(apps_data) if apps_data else 0} apps")
            
            # 샘플 데이터인지 확인 (YouTube, Instagram만 있는 경우)
            if apps_data and len(apps_data) <= 2:
                app_names = [app.get("name", "") for app in apps_data]
                if "YouTube" in app_names or "Instagram" in app_names:
                    logger.warning(f"Only sample apps returned (likely google-play-scraper not working). Apps: {app_names}")
                    # 샘플 데이터라도 분석은 진행하지만 경고 메시지 추가
        except Exception as e:
            logger.error(f"Error fetching apps: {e}", exc_info=True)
            import traceback
            error_detail = traceback.format_exc()
            logger.error(f"Traceback: {error_detail}")
            raise HTTPException(
                status_code=500,
                detail=f"앱 데이터를 가져오는 중 오류가 발생했습니다: {str(e)}"
            )
        
        if not apps_data:
            logger.warning(f"No apps data returned for category {play_category}")
            raise HTTPException(
                status_code=500, 
                detail="앱 데이터를 가져올 수 없습니다. google-play-scraper 라이브러리가 Railway에서 작동하지 않을 수 있습니다."
            )
        
        # GPT로 분석
        try:
            analysis_result = await analyze_category_with_gpt(
                apps_data=apps_data,
                category_name=play_category,
                limit=limit
            )
            logger.info(f"GPT analysis result: success={analysis_result.get('success')}")
        except Exception as e:
            logger.error(f"Error in GPT analysis: {e}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"GPT 분석 중 오류가 발생했습니다: {str(e)}"
            )
        
        if not analysis_result.get("success"):
            error_msg = analysis_result.get("error", "분석 실패")
            logger.error(f"GPT analysis failed: {error_msg}")
            # 더 자세한 에러 정보 제공
            detailed_error = f"{error_msg}"
            if "OpenAI API 키" in error_msg or "API key" in error_msg.lower():
                detailed_error += " Railway 환경 변수에서 OPENAI_API_KEY를 확인해주세요."
            raise HTTPException(status_code=500, detail=detailed_error)
        
        return analysis_result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in analyze_category: {e}", exc_info=True)
        import traceback
        error_detail = traceback.format_exc()
        logger.error(f"Traceback: {error_detail}")
        raise HTTPException(
            status_code=500,
            detail=f"카테고리 분석 실패: {str(e)}"
        )


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
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        # Play Store 앱만 조회
        latest_app = db.query(App).filter(
            App.package_name.isnot(None),
            App.package_name != ""
        ).order_by(App.id.desc()).first()
        
        if not latest_app:
            logger.info("No Play Store apps found in database")
            return {
                "last_fetch": None,
                "message": "아직 앱 데이터를 가져온 적이 없습니다."
            }
        
        kst = ZoneInfo("Asia/Seoul")
        now = datetime.now(kst)
        days_until_monday = (7 - now.weekday()) % 7
        if days_until_monday == 0:
            if now.hour < 9:
                next_monday = now.replace(hour=9, minute=0, second=0, microsecond=0)
            else:
                next_monday = (now.replace(hour=9, minute=0, second=0, microsecond=0) + 
                              timedelta(days=7))
        else:
            next_monday = (now.replace(hour=9, minute=0, second=0, microsecond=0) + 
                          timedelta(days=days_until_monday))
        
        try:
            can_fetch_now = should_fetch_this_week()
        except Exception as e:
            logger.warning(f"Error checking should_fetch_this_week: {e}")
            can_fetch_now = False
        
        # created_at 필드가 있으면 사용, 없으면 None
        last_fetch = None
        if hasattr(latest_app, 'created_at'):
            created_at_value = getattr(latest_app, 'created_at', None)
            if created_at_value:
                try:
                    if isinstance(created_at_value, datetime):
                        last_fetch = created_at_value.isoformat()
                    else:
                        last_fetch = str(created_at_value)
                except Exception as e:
                    logger.warning(f"Error formatting created_at: {e}")
                    last_fetch = None
        
        logger.info(f"Last fetch info retrieved: last_fetch={last_fetch}, can_fetch_now={can_fetch_now}")
        
        return {
            "last_fetch": last_fetch,
            "next_scheduled_fetch": next_monday.isoformat(),
            "can_fetch_now": can_fetch_now
        }
    except Exception as e:
        logger.error(f"Error in get_last_fetch_info: {e}", exc_info=True)
        import traceback
        error_detail = traceback.format_exc()
        logger.error(f"Traceback: {error_detail}")
        raise HTTPException(
            status_code=500,
            detail=f"마지막 수집 정보를 가져오는 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/mvp-productivity-apps")
async def get_mvp_productivity_apps(
    limit: int = 10,
    max_difficulty: float = 1.5,
    min_marketability: float = 5.0,
    max_features: int = 5,
    db: Session = Depends(get_db)
):
    """
    생산성, 라이프스타일, 도구 카테고리의 무료 앱 중 MVP에 가깝고 난이도가 낮은 앱 목록 자동 생성
    
    기본 설정:
    - 카테고리: 생산성, 라이프스타일, 도구 (순환)
    - 각 카테고리당 앱 수: 10개 (기본값)
    - 가격 모델: 무료
    - 난이도: max_difficulty 이하
    - 시장성: min_marketability 이상
    - 기능 수: max_features 이하
    """
    import logging
    logger = logging.getLogger(__name__)
    
    # 기본 카테고리 목록 (순환)
    default_categories = [
        "APPLICATION_PRODUCTIVITY",  # 생산성
        "APPLICATION_LIFESTYLE",     # 라이프스타일
        "APPLICATION_TOOLS"          # 도구
    ]
    
    category_names = {
        "APPLICATION_PRODUCTIVITY": "생산성",
        "APPLICATION_LIFESTYLE": "라이프스타일",
        "APPLICATION_TOOLS": "도구"
    }
    
    try:
        all_filtered_apps = []
        
        # 각 카테고리별로 처리
        for category_key in default_categories:
            category_name = category_names.get(category_key, category_key)
            logger.info(f"Processing category: {category_name} ({category_key})")
            
            # 1. 해당 카테고리의 무료 앱 가져오기 (DB에 없으면 스크래핑)
            category_apps = db.query(App).filter(
                App.package_name.isnot(None),
                App.package_name != "",
                App.price_model == "free",
                App.category == category_key
            ).all()
            
            # DB에 앱이 적으면 자동으로 가져오기
            if len(category_apps) < limit:
                logger.info(f"{category_name} apps in DB are insufficient ({len(category_apps)} < {limit}), fetching from Play Store...")
                try:
                    apps_data = await fetch_top_apps(
                        category="top_free",
                        limit=limit * 2,  # 여유있게 가져오기
                        play_category=category_key
                    )
                    
                    # 앱 저장 및 점수 계산
                    from app.services.pipeline import normalize_app_data, store_apps
                    normalized = normalize_app_data(apps_data)
                    store_result = store_apps(normalized, db, update_existing=True)
                    logger.info(f"Stored {store_result.get('saved_count', 0)} {category_name} apps")
                    
                    # 다시 조회
                    category_apps = db.query(App).filter(
                        App.package_name.isnot(None),
                        App.package_name != "",
                        App.price_model == "free",
                        App.category == category_key
                    ).all()
                except Exception as e:
                    logger.error(f"Error fetching {category_name} apps: {e}", exc_info=True)
            
            # 2. 필터링: 난이도, 시장성, 기능 수
            filtered_apps = []
            for app in category_apps:
                # 난이도가 없으면 설명 기반으로 추정
                if app.difficulty_score is None or app.difficulty_score == 0.0:
                    from app.services.difficulty_scorer import estimate_difficulty_from_description
                    estimated_difficulty = estimate_difficulty_from_description(app.description or "")
                    if estimated_difficulty > max_difficulty:
                        continue
                    # 추정된 난이도로 업데이트 (다음 조회 시 사용)
                    app.difficulty_score = estimated_difficulty
                    db.commit()
                elif app.difficulty_score > max_difficulty:
                    continue
                
                # 시장성 체크
                if app.marketability_score is None or app.marketability_score < min_marketability:
                    continue
                
                # 기능 수 체크 (MVP에 가까운 앱) - 기능이 없어도 설명 기반으로 추정 가능한 앱은 포함
                feature_count = len(app.features) if app.features else 0
                if feature_count > max_features:
                    continue
                
                filtered_apps.append(app)
            
            # 3. 정렬: 효율성 순 (시장성 높고 난이도 낮은 순)
            filtered_apps.sort(
                key=lambda a: (
                    -(a.marketability_score or 0),  # 시장성 높은 순
                    a.difficulty_score or 999  # 난이도 낮은 순
                )
            )
            
            # 4. 각 카테고리에서 limit개만 선택
            category_result = filtered_apps[:limit]
            all_filtered_apps.extend(category_result)
            logger.info(f"{category_name}: Found {len(filtered_apps)} apps, selected {len(category_result)}")
        
        # 5. 전체 결과를 다시 정렬 (시장성 높고 난이도 낮은 순)
        all_filtered_apps.sort(
            key=lambda a: (
                -(a.marketability_score or 0),  # 시장성 높은 순
                a.difficulty_score or 999  # 난이도 낮은 순
            )
        )
        
        # 6. 응답 형식 변환
        return [
            {
                "id": app.id,
                "name": app.name,
                "package_name": app.package_name,
                "category": app.category,
                "category_name": category_names.get(app.category, app.category),
                "rating": app.rating,
                "review_count": app.review_count,
                "price_model": app.price_model,
                "description": app.description,
                "difficulty_score": app.difficulty_score,
                "marketability_score": app.marketability_score,
                "feature_count": len(app.features) if app.features else 0,
                "created_at": app.created_at.isoformat() if app.created_at else None
            }
            for app in all_filtered_apps
        ]
        
    except Exception as e:
        logger.error(f"Error in get_mvp_productivity_apps: {e}", exc_info=True)
        import traceback
        error_detail = traceback.format_exc()
        logger.error(f"Traceback: {error_detail}")
        raise HTTPException(
            status_code=500,
            detail=f"MVP 앱 목록을 가져오는 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/status")
async def get_fetch_status(db: Session = Depends(get_db)):
    """
    현재 앱 순위를 가져올 수 있는지 상태 확인
    """
    current_time = datetime.now(ZoneInfo("Asia/Seoul"))
    weekday_names = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    
    # 다음 월요일 계산
    days_until_monday = (7 - current_time.weekday()) % 7
    if days_until_monday == 0:
        if current_time.hour < 9:
            next_monday = current_time.replace(hour=9, minute=0, second=0, microsecond=0)
        else:
            next_monday = (current_time.replace(hour=9, minute=0, second=0, microsecond=0) + 
                          timedelta(days=7))
    else:
        next_monday = (current_time.replace(hour=9, minute=0, second=0, microsecond=0) + 
                      timedelta(days=days_until_monday))
    
    try:
        can_fetch = should_fetch_this_week()
    except Exception as e:
        can_fetch = False
    
    return {
        "current_time": current_time.isoformat(),
        "current_weekday": weekday_names[current_time.weekday()],
        "can_fetch": can_fetch,
        "next_monday": next_monday.isoformat(),
        "timezone": "GMT+9 (Asia/Seoul)"
    }
