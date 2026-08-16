#!/usr/bin/env python3
"""
앱 수집 및 분석 상태 확인 스크립트
"""
import sys
import asyncio
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

# 프로젝트 경로 추가
sys.path.insert(0, '/Users/donghakim/Desktop/application/016-Application-market-analytics')

from app.database import SessionLocal, engine
from app.models import App, Feature, AppType
from app.services.pipeline import store_apps, normalize_app_data

def check_database_status():
    """데이터베이스 상태 확인"""
    db = SessionLocal()
    try:
        # 전체 앱 수
        total_apps = db.query(App).count()
        print(f"\n📊 데이터베이스 상태:")
        print(f"  - 전체 앱 수: {total_apps}")
        
        # 카테고리별 앱 수
        if total_apps > 0:
            categories = db.query(App.category, func.count(App.id).label('count')).group_by(App.category).all()
            print(f"\n📁 카테고리별 앱 수:")
            for cat, count in categories:
                print(f"  - {cat or 'Unknown'}: {count}개")
            
            # 난이도 점수가 있는 앱
            apps_with_difficulty = db.query(App).filter(App.difficulty_score > 0).count()
            print(f"\n🎯 분석 상태:")
            print(f"  - 난이도 점수가 있는 앱: {apps_with_difficulty}개")
            
            # 시장성 점수가 있는 앱
            apps_with_marketability = db.query(App).filter(App.marketability_score > 0).count()
            print(f"  - 시장성 점수가 있는 앱: {apps_with_marketability}개")
            
            # 최근 수집된 앱 (상위 10개)
            recent_apps = db.query(App).order_by(App.created_at.desc()).limit(10).all()
            print(f"\n🕐 최근 수집된 앱 (상위 10개):")
            for app in recent_apps:
                difficulty = app.difficulty_score or 0
                marketability = app.marketability_score or 0
                print(f"  - {app.name} (난이도: {difficulty:.2f}, 시장성: {marketability:.2f}, 카테고리: {app.category})")
            
            # 난이도가 낮은 앱 (1.0 이하)
            low_difficulty = db.query(App).filter(App.difficulty_score <= 1.0).count()
            print(f"\n✨ 난이도가 낮은 앱 (1.0 이하): {low_difficulty}개")
            
            # 기능이 있는 앱
            apps_with_features = db.query(App).join(Feature).distinct().count()
            print(f"  - 기능이 있는 앱: {apps_with_features}개")
            
            # 앱 타입 수
            app_types_count = db.query(AppType).count()
            print(f"\n📋 분석된 앱 타입 수: {app_types_count}개")
            
            if app_types_count > 0:
                app_types = db.query(AppType).all()
                print(f"\n🏷️ 앱 타입 목록:")
                for app_type in app_types:
                    print(f"  - {app_type.name} (난이도: {app_type.avg_difficulty:.2f}, 시장성: {app_type.avg_marketability:.2f}, 앱 수: {app_type.app_count})")
        
    except Exception as e:
        print(f"❌ 데이터베이스 확인 중 오류: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

def check_recent_collection():
    """최근 수집 상태 확인"""
    db = SessionLocal()
    try:
        # 생산성 앱
        productivity = db.query(App).filter(App.category == "APPLICATION_PRODUCTIVITY").count()
        print(f"\n💼 생산성 앱: {productivity}개")
        
        # 라이프스타일 앱
        lifestyle = db.query(App).filter(App.category == "APPLICATION_LIFESTYLE").count()
        print(f"🏠 라이프스타일 앱: {lifestyle}개")
        
        # 도구 앱
        tools = db.query(App).filter(App.category == "APPLICATION_TOOLS").count()
        print(f"🔧 도구 앱: {tools}개")
        
        # YouTube/Instagram 제외 확인
        youtube_instagram = db.query(App).filter(
            (App.package_name.ilike('%youtube%')) | 
            (App.package_name.ilike('%instagram%')) |
            (App.name.ilike('%YouTube%')) |
            (App.name.ilike('%Instagram%'))
        ).count()
        print(f"🚫 YouTube/Instagram 앱 수: {youtube_instagram}개 (제외되어야 함)")
        
    except Exception as e:
        print(f"❌ 수집 상태 확인 중 오류: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("🔍 앱 수집 및 분석 상태 확인")
    print("=" * 60)
    
    check_database_status()
    check_recent_collection()
    
    print("\n" + "=" * 60)
    print("✅ 확인 완료")
    print("=" * 60)
