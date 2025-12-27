from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
from io import StringIO
from datetime import datetime
from typing import List
from app.database import get_db
from app.models import App
from app.services.marketability_scorer import calculate_marketability_score, parse_date

router = APIRouter(prefix="/api/upload", tags=["upload"])


@router.post("/csv")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    CSV 파일 업로드하여 앱 데이터 일괄 생성
    
    CSV 형식:
    name, category, rating, review_count, price_model, last_update, description
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="CSV 파일만 업로드 가능합니다.")
    
    try:
        # CSV 파일 읽기
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode('utf-8')))
        
        # 필수 컬럼 확인
        required_columns = ['name']
        if not all(col in df.columns for col in required_columns):
            raise HTTPException(
                status_code=400,
                detail=f"필수 컬럼이 없습니다: {required_columns}"
            )
        
        created_apps = []
        errors = []
        
        for idx, row in df.iterrows():
            try:
                # 날짜 파싱
                last_update = None
                if 'last_update' in row and pd.notna(row['last_update']):
                    last_update = parse_date(str(row['last_update']))
                
                # 앱 데이터 생성
                app_data = {
                    "name": str(row['name']),
                    "category": str(row['category']) if 'category' in row and pd.notna(row.get('category')) else None,
                    "rating": float(row['rating']) if 'rating' in row and pd.notna(row.get('rating')) else None,
                    "review_count": int(row['review_count']) if 'review_count' in row and pd.notna(row.get('review_count')) else None,
                    "price_model": str(row['price_model']) if 'price_model' in row and pd.notna(row.get('price_model')) else None,
                    "last_update": last_update,
                    "description": str(row['description']) if 'description' in row and pd.notna(row.get('description')) else None
                }
                
                # 시장성 점수 계산
                marketability_score = calculate_marketability_score(
                    review_count=app_data['review_count'] or 0,
                    rating=app_data['rating'] or 0.0,
                    last_update=last_update.isoformat() if last_update else None,
                    price_model=app_data['price_model'],
                    description=app_data['description'] or ""
                )
                
                # 앱 생성
                db_app = App(**app_data, marketability_score=marketability_score)
                db.add(db_app)
                db.flush()
                
                created_apps.append({
                    "id": db_app.id,
                    "name": db_app.name
                })
                
            except Exception as e:
                errors.append({
                    "row": idx + 2,  # 헤더 포함 +1, 0-indexed +1
                    "error": str(e)
                })
        
        db.commit()
        
        return {
            "message": f"{len(created_apps)}개의 앱이 생성되었습니다.",
            "created_count": len(created_apps),
            "created_apps": created_apps,
            "errors": errors if errors else None
        }
        
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="CSV 파일이 비어있습니다.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 처리 중 오류 발생: {str(e)}")




