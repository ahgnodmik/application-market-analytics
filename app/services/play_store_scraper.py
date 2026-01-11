"""
Google Play Store 앱 순위 크롤러
매주 월요일 GMT+9 기준으로 상위 앱 데이터를 가져옵니다.
"""
import httpx
import re
from typing import List, Dict, Optional
from datetime import datetime
import time


async def fetch_top_apps(category: str = "top_free", limit: int = 100) -> List[Dict]:
    """
    Google Play Store에서 상위 앱 목록 가져오기
    
    Args:
        category: 카테고리 ("top_free", "top_paid", "top_grossing" 등)
        limit: 가져올 앱 수 (최대 100)
    
    Returns:
        앱 정보 리스트
    """
    # Google Play Store는 공식 API가 제한적이므로
    # 웹 스크래핑 또는 서드파티 API 사용
    # 예시: AppBrain, AppAnnie 등 서드파티 서비스 사용
    # 또는 직접 Play Store 페이지 크롤링
    
    apps = []
    
    try:
        # Google Play Store Top Charts URL
        # 실제 구현은 Play Store 구조에 따라 달라질 수 있습니다
        base_url = "https://play.google.com/store/apps"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # 카테고리별 URL 구성
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
                # HTML 파싱 (실제 구현 필요)
                # BeautifulSoup 등을 사용하여 앱 정보 추출
                apps = parse_play_store_html(response.text, limit)
            else:
                print(f"Error fetching Play Store data: {response.status_code}")
                
    except Exception as e:
        print(f"Error in fetch_top_apps: {e}")
        # 폴백: 샘플 데이터 반환 (실제 구현 시 제거)
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
        # 예시: 앱 카드 찾기
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
                print(f"Error parsing app card: {e}")
                continue
        
        # 파싱한 앱이 없으면 샘플 데이터 반환
        if not apps:
            return get_sample_apps(limit)
            
        return apps[:limit]
    except ImportError:
        print("BeautifulSoup not installed, using sample data")
        return get_sample_apps(limit)
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return get_sample_apps(limit)


def extract_package_name(href: str) -> str:
    """URL에서 패키지 이름 추출"""
    match = re.search(r'id=([^&]+)', href)
    return match.group(1) if match else ""


def extract_category(card) -> str:
    """카드에서 카테고리 추출"""
    # 실제 구현 필요
    return "General"


def extract_rating(card) -> float:
    """카드에서 평점 추출"""
    # 실제 구현 필요
    return 4.0


def extract_review_count(card) -> int:
    """카드에서 리뷰 수 추출"""
    # 실제 구현 필요
    return 10000


def extract_price_model(card) -> str:
    """카드에서 가격 모델 추출"""
    # 실제 구현 필요
    return "free"


def extract_description(card) -> str:
    """카드에서 설명 추출"""
    # 실제 구현 필요
    return ""


def get_sample_apps(limit: int = 100) -> List[Dict]:
    """
    샘플 앱 데이터 (실제 구현 전 임시)
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
        # 추가 샘플 데이터...
    ]
    
    return sample_apps[:limit]


async def fetch_app_details(package_name: str) -> Optional[Dict]:
    """
    특정 앱의 상세 정보 가져오기
    
    Args:
        package_name: 앱 패키지 이름 (예: com.google.android.youtube)
    
    Returns:
        앱 상세 정보
    """
    try:
        url = f"https://play.google.com/store/apps/details?id={package_name}"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            
            if response.status_code == 200:
                # HTML 파싱하여 상세 정보 추출
                return parse_app_details(response.text)
            else:
                return None
                
    except Exception as e:
        print(f"Error fetching app details: {e}")
        return None


def parse_app_details(html: str) -> Dict:
    """
    앱 상세 페이지 HTML 파싱
    """
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
    
    # GMT+9 타임존 설정
    from zoneinfo import ZoneInfo
    kst = ZoneInfo("Asia/Seoul")
    current_kst = current_time.astimezone(kst)
    
    # 월요일인지 확인 (월요일 = 0)
    if current_kst.weekday() == 0:
        # 월요일이면 가져오기
        # 추가 조건: 특정 시간(예: 오전 9시) 이후인지 확인 가능
        return True
    
    return False
