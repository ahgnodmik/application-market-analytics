from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.database import get_db
from app.models import App, Feature
from app.services.openai_service import analyze_apps_with_ai, generate_single_app_analysis
from app.schemas import AppResponse

router = APIRouter(prefix="/api/report", tags=["report"])


class ReportRequest(BaseModel):
    app_ids: Optional[List[int]] = None  # None이면 모든 앱 분석


@router.post("/generate")
async def generate_report(request: ReportRequest = None, db: Session = Depends(get_db)):
    """
    ChatGPT를 사용하여 앱 마켓 분석 리포트 생성
    """
    try:
        # 앱 데이터 조회
        if request and request.app_ids:
            apps = db.query(App).filter(App.id.in_(request.app_ids)).all()
        else:
            apps = db.query(App).all()
        
        if not apps:
            raise HTTPException(status_code=400, detail="분석할 앱이 없습니다.")
        
        # 앱 데이터 변환
        apps_data = []
        for app in apps:
            features = db.query(Feature).filter(Feature.app_id == app.id).all()
            app_dict = {
                "id": app.id,
                "name": app.name,
                "category": app.category,
                "rating": app.rating,
                "review_count": app.review_count,
                "price_model": app.price_model,
                "description": app.description,
                "difficulty_score": app.difficulty_score,
                "marketability_score": app.marketability_score,
                "features": [
                    {
                        "name": f.name,
                        "feature_type": f.feature_type,
                        "difficulty_score": f.difficulty_score
                    }
                    for f in features
                ]
            }
            apps_data.append(app_dict)
        
        # AI 분석 실행
        result = analyze_apps_with_ai(apps_data)
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error", "AI 분석 실패"))
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"리포트 생성 중 오류: {str(e)}")


@router.post("/analyze-app/{app_id}")
async def analyze_single_app(app_id: int, db: Session = Depends(get_db)):
    """
    단일 앱에 대한 상세 AI 분석
    """
    app = db.query(App).filter(App.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="앱을 찾을 수 없습니다.")
    
    features = db.query(Feature).filter(Feature.app_id == app.id).all()
    
    app_data = {
        "id": app.id,
        "name": app.name,
        "category": app.category,
        "rating": app.rating,
        "review_count": app.review_count,
        "price_model": app.price_model,
        "description": app.description,
        "difficulty_score": app.difficulty_score,
        "marketability_score": app.marketability_score,
        "features": [
            {
                "name": f.name,
                "feature_type": f.feature_type,
                "difficulty_score": f.difficulty_score
            }
            for f in features
        ]
    }
    
    try:
        result = generate_single_app_analysis(app_data)
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error", "AI 분석 실패"))
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 중 오류: {str(e)}")

