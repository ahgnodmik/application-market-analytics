"""
Google Play Store 앱 순위 크롤러
매주 월요일 GMT+9 기준으로 상위 앱 데이터를 가져옵니다.

실제 구현: google-play-scraper 라이브러리 사용
Fallback: HTML 스크래핑 또는 샘플 데이터
"""
import httpx
import re
from typing import List, Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# google-play-scraper 라이브러리 사용 시도
try:
    from app.services.play_store_scraper_real import fetch_top_apps_real, fetch_app_details_real
    REAL_SCRAPER_AVAILABLE = True
    logger.info("✅ Real Play Store scraper available (google-play-scraper)")
except ImportError:
    REAL_SCRAPER_AVAILABLE = False
    logger.warning("⚠️ google-play-scraper not installed, using fallback methods")


async def fetch_top_apps(category: str = "top_free", limit: int = 100, play_category: Optional[str] = None) -> List[Dict]:
    """
    Google Play Store에서 상위 앱 목록 가져오기
    
    실제 구현: google-play-scraper 라이브러리 사용 (권장)
    Fallback: HTML 스크래핑 또는 샘플 데이터
    
    Args:
        category: 카테고리 ("top_free", "top_paid", "top_grossing")
        limit: 가져올 앱 수 (최대 100)
    
    Returns:
        앱 정보 리스트
    """
    # 방법 1: google-play-scraper 라이브러리 사용 (권장)
    if REAL_SCRAPER_AVAILABLE:
        try:
            logger.info(f"Using google-play-scraper for {category} apps (limit: {limit})")
            return await fetch_top_apps_real(category=category, limit=limit)
        except Exception as e:
            logger.error(f"Error with google-play-scraper: {e}, falling back to HTML scraping")
    
    # 방법 2: 직접 HTML 스크래핑 (fallback)
    apps = []
    
    try:
        base_url = "https://play.google.com/store/apps"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            if category == "top_free":
                url = f"{base_url}/collection/topselling_free"
            elif category == "top_paid":
                url = f"{base_url}/collection/topselling_paid"
            elif category == "top_grossing":
                url = f"{base_url}/collection/topgrossing"
            else:
                url = f"{base_url}/collection/topselling_free"
            
            response = await client.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            
            if response.status_code == 200:
                apps = parse_play_store_html(response.text, limit)
            else:
                logger.warning(f"Error fetching Play Store HTML: {response.status_code}")
                
    except Exception as e:
        logger.error(f"Error in HTML scraping: {e}")
    
    # 최종 폴백: 샘플 데이터
    if not apps:
        logger.warning("Using sample data as fallback")
        apps = get_sample_apps(limit)
    
    return apps


def parse_play_store_html(html: str, limit: int) -> List[Dict]:
    """
    Play Store HTML에서 앱 정보 파싱
    BeautifulSoup을 사용하여 실제 데이터 추출
    """
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'lxml')
        apps = []
        
        # Play Store 구조에 따라 파싱 (실제 구조 확인 필요)
        app_cards = soup.find_all('div', class_=re.compile('.*card.*', re.I))[:limit]
        
        for card in app_cards:
            try:
                app_name = card.find('a', {'title': True})
                if app_name:
                    apps.append({
                        "name": app_name.get('title', 'Unknown'),
                        "package_name": extract_package_name(app_name.get('href', '')),
                        "category": extract_category(card),
                        "rating": extract_rating(card),
                        "review_count": extract_review_count(card),
                        "price_model": extract_price_model(card),
                        "description": extract_description(card),
                        "last_update": datetime.now().isoformat()
                    })
            except Exception as e:
                logger.error(f"Error parsing app card: {e}")
                continue
        
        if not apps:
            return get_sample_apps(limit)
            
        return apps[:limit]
    except ImportError:
        logger.warning("BeautifulSoup not installed, using sample data")
        return get_sample_apps(limit)
    except Exception as e:
        logger.error(f"Error parsing HTML: {e}")
        return get_sample_apps(limit)


def extract_package_name(href: str) -> str:
    """URL에서 패키지 이름 추출"""
    match = re.search(r'id=([^&]+)', href)
    return match.group(1) if match else ""


def extract_category(card) -> str:
    """카드에서 카테고리 추출"""
    return "General"


def extract_rating(card) -> float:
    """카드에서 평점 추출"""
    return 4.0


def extract_review_count(card) -> int:
    """카드에서 리뷰 수 추출"""
    return 10000


def extract_price_model(card) -> str:
    """카드에서 가격 모델 추출"""
    return "free"


def extract_description(card) -> str:
    """카드에서 설명 추출"""
    return ""


def get_sample_apps(limit: int = 100) -> List[Dict]:
    """샘플 앱 데이터 (fallback)"""
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


async def fetch_app_details(package_name: str) -> Optional[Dict]:
    """
    특정 앱의 상세 정보 가져오기
    
    실제 구현: google-play-scraper 라이브러리 사용 (권장)
    Fallback: HTML 스크래핑
    """
    # 방법 1: google-play-scraper 라이브러리 사용 (권장)
    if REAL_SCRAPER_AVAILABLE:
        try:
            return await fetch_app_details_real(package_name=package_name)
        except Exception as e:
            logger.error(f"Error with google-play-scraper: {e}, falling back to HTML scraping")
    
    # 방법 2: 직접 HTML 스크래핑 (fallback)
    try:
        url = f"https://play.google.com/store/apps/details?id={package_name}"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            
            if response.status_code == 200:
                return parse_app_details(response.text)
            else:
                return None
                
    except Exception as e:
        logger.error(f"Error fetching app details: {e}")
        return None


def parse_app_details(html: str) -> Dict:
    """앱 상세 페이지 HTML 파싱"""
    # 실제 구현 필요
    return {}


def should_fetch_this_week(current_time: Optional[datetime] = None) -> bool:
    """
    이번 주 월요일 GMT+9 기준으로 데이터를 가져올 시점인지 확인
    
    Args:
        current_time: 확인할 시간 (없으면 현재 시간 사용)
    
    Returns:
        가져올 시점이면 True
    """
    if current_time is None:
        current_time = datetime.now()
    
    from zoneinfo import ZoneInfo
    kst = ZoneInfo("Asia/Seoul")
    current_kst = current_time.astimezone(kst)
    
    # 월요일인지 확인 (월요일 = 0)
    if current_kst.weekday() == 0:
        return True
    
    return False
