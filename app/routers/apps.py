"""
앱 관리 라우터
Play Store에서 가져온 앱들을 관리
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import or_
import logging

from app.database import get_db
from app.models import App
from app.schemas import AppResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/apps", tags=["apps"])


@router.get("/", response_model=List[AppResponse])
async def get_apps(
    source: Optional[str] = None,  # "playstore" 또는 None (모두)
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    앱 목록 조회
    source="playstore"일 경우 Play Store에서 가져온 앱만 반환
    """
    try:
        query = db.query(App)
        
        # Play Store 앱만 필터링 (package_name이 있는 것)
        if source == "playstore":
            query = query.filter(App.package_name.isnot(None), App.package_name != "")
        
        apps = query.order_by(App.id.desc()).offset(skip).limit(limit).all()
        logger.info(f"Found {len(apps)} apps (source={source}, skip={skip}, limit={limit})")
        return apps if apps else []
    except Exception as e:
        logger.error(f"Error in get_apps: {e}", exc_info=True)
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"앱 목록을 불러오는 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/playstore", response_model=List[AppResponse])
async def get_playstore_apps(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Play Store에서 가져온 앱 목록만 조회
    """
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        # 데이터베이스 쿼리
        query = db.query(App).filter(
            App.package_name.isnot(None),
            App.package_name != ""
        )
        
        apps = query.order_by(App.id.desc()).offset(skip).limit(limit).all()
        
        logger.info(f"Found {len(apps)} Play Store apps (skip={skip}, limit={limit})")
        
        # 빈 리스트도 정상적인 응답
        return apps if apps else []
        
    except Exception as e:
        logger.error(f"Error in get_playstore_apps: {e}", exc_info=True)
        import traceback
        error_detail = traceback.format_exc()
        logger.error(f"Traceback: {error_detail}")
        
        # 에러 응답을 JSON으로 반환
        raise HTTPException(
            status_code=500,
            detail=f"앱 목록을 불러오는 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/{app_id}", response_model=AppResponse)
async def get_app(app_id: int, db: Session = Depends(get_db)):
    """앱 상세 정보 조회"""
    try:
        app = db.query(App).filter(App.id == app_id).first()
        if not app:
            raise HTTPException(status_code=404, detail="App not found")
        return app
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_app: {e}", exc_info=True)
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"앱 상세 정보를 불러오는 중 오류가 발생했습니다: {str(e)}"
        )
