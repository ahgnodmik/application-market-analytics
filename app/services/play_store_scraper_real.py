"""
Google Play Store 앱 순위 크롤러 (실제 구현)
google-play-scraper 라이브러리 사용
"""
from typing import List, Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

try:
    from google_play_scraper import collections, Collection, Category
    SCRAPER_AVAILABLE = True
except ImportError:
    SCRAPER_AVAILABLE = False
    logger.warning("google-play-scraper not installed, using fallback")


async def fetch_top_apps_real(
    category: str = "top_free",
    limit: int = 100,
    country: str = "kr",
    lang: str = "ko"
) -> List[Dict]:
    """
    Google Play Store에서 상위 앱 목록 가져오기 (실제 구현)
    
    Args:
        category: 카테고리 ("top_free", "top_paid", "top_grossing")
        limit: 가져올 앱 수 (최대 100)
        country: 국가 코드 (기본값: "kr" - 한국)
        lang: 언어 코드 (기본값: "ko" - 한국어)
    
    Returns:
        앱 정보 리스트
    """
    if not SCRAPER_AVAILABLE:
        logger.error("google-play-scraper not available, cannot fetch real data")
        return get_sample_apps(limit)
    
    try:
        # Collection 타입 선택
        if category == "top_free":
            collection_type = Collection.TOP_FREE
        elif category == "top_paid":
            collection_type = Collection.TOP_PAID
        elif category == "top_grossing":
            collection_type = Collection.TOP_GROSSING
        else:
            collection_type = Collection.TOP_FREE
        
        # 상위 앱 가져오기
        logger.info(f"Fetching {category} apps from Play Store (limit: {limit})...")
        apps_data = collections(
            collection=collection_type,
            category=Category.APPLICATION,  # 모든 앱 카테고리
            results=min(limit, 250),  # 최대 250개까지 가능
            lang=lang,
            country=country
        )
        
        # 데이터 형식 변환
        parsed_apps = []
        for app_info in apps_data:
            try:
                # 설치 수를 숫자로 변환
                installs_text = app_info.get('installs', '0')
                review_count = parse_installs_to_number(installs_text)
                
                app_dict = {
                    "name": app_info.get('title', 'Unknown'),
                    "package_name": app_info.get('appId', ''),
                    "category": app_info.get('genre', ''),
                    "rating": float(app_info.get('score', 0.0)),
                    "review_count": review_count,
                    "price_model": determine_price_model(app_info),
                    "description": app_info.get('description', ''),
                    "last_update": app_info.get('updated', datetime.now()).isoformat() if isinstance(app_info.get('updated'), datetime) else datetime.now().isoformat(),
                    "icon": app_info.get('icon', ''),
                    "developer": app_info.get('developer', ''),
                }
                parsed_apps.append(app_dict)
                
            except Exception as e:
                logger.error(f"Error parsing app {app_info.get('title', 'Unknown')}: {e}")
                continue
        
        logger.info(f"Successfully fetched {len(parsed_apps)} apps from Play Store")
        return parsed_apps[:limit]
        
    except Exception as e:
        logger.error(f"Error fetching Play Store data: {e}")
        import traceback
        logger.error(traceback.format_exc())
        # 폴백: 샘플 데이터 반환
        return get_sample_apps(limit)


def parse_installs_to_number(installs_text: str) -> int:
    """
    설치 수 텍스트를 숫자로 변환
    예: "1,000,000+" -> 1000000
    """
    try:
        # 숫자와 쉼표 제거
        cleaned = installs_text.replace(',', '').replace('+', '').strip()
        if cleaned:
            return int(cleaned)
        return 0
    except:
        return 0


def determine_price_model(app_info: Dict) -> str:
    """
    앱 정보에서 가격 모델 결정
    """
    price = app_info.get('price', 0)
    if price == 0 or price == '0':
        return "free"
    elif app_info.get('free', True):
        return "free"
    else:
        # 구독 또는 일회성 결제 구분 필요
        # 일단 paid로 처리
        return "paid"


async def fetch_app_details_real(package_name: str, country: str = "kr", lang: str = "ko") -> Optional[Dict]:
    """
    특정 앱의 상세 정보 가져오기 (실제 구현)
    
    Args:
        package_name: 앱 패키지 이름
        country: 국가 코드
        lang: 언어 코드
    
    Returns:
        앱 상세 정보
    """
    if not SCRAPER_AVAILABLE:
        return None
    
    try:
        from google_play_scraper import app
        
        app_info = app(
            package_name,
            lang=lang,
            country=country
        )
        
        # 데이터 형식 변환
        installs_text = app_info.get('installs', '0')
        review_count = parse_installs_to_number(installs_text)
        
        return {
            "name": app_info.get('title', 'Unknown'),
            "package_name": app_info.get('appId', package_name),
            "category": app_info.get('genre', ''),
            "rating": float(app_info.get('score', 0.0)),
            "review_count": review_count,
            "price_model": determine_price_model(app_info),
            "description": app_info.get('description', ''),
            "last_update": app_info.get('updated', datetime.now()).isoformat() if isinstance(app_info.get('updated'), datetime) else datetime.now().isoformat(),
            "icon": app_info.get('icon', ''),
            "developer": app_info.get('developer', ''),
            "content_rating": app_info.get('contentRating', ''),
            "size": app_info.get('size', ''),
        }
        
    except Exception as e:
        logger.error(f"Error fetching app details for {package_name}: {e}")
        return None


def get_sample_apps(limit: int = 100) -> List[Dict]:
    """
    샘플 앱 데이터 (fallback)
    """
    sample_apps = [
        {
            "name": "YouTube",
            "package_name": "com.google.android.youtube",
            "category": "Video Players & Editors",
            "rating": 4.4,
            "review_count": 50000000,
            "price_model": "free",
            "description": "세계 최대 동영상 플랫폼",
            "last_update": datetime.now().isoformat()
        },
        {
            "name": "Instagram",
            "package_name": "com.instagram.android",
            "category": "Social",
            "rating": 4.5,
            "review_count": 30000000,
            "price_model": "free",
            "description": "사진 및 동영상 공유 소셜 네트워크",
            "last_update": datetime.now().isoformat()
        },
    ]
    
    return sample_apps[:limit]
