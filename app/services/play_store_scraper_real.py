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
    Category = None
    Collection = None
    logger.warning("google-play-scraper not installed, using fallback")


# 기본 카테고리 목록 (라이브러리가 없을 때도 사용 가능)
DEFAULT_CATEGORIES = [
    {"key": "APPLICATION", "name": "Application", "type": "APPLICATION"},
    {"key": "GAME", "name": "Game", "type": "GAME"},
    {"key": "APPLICATION_SOCIAL", "name": "Social", "type": "APPLICATION"},
    {"key": "APPLICATION_PRODUCTIVITY", "name": "Productivity", "type": "APPLICATION"},
    {"key": "APPLICATION_ENTERTAINMENT", "name": "Entertainment", "type": "APPLICATION"},
    {"key": "APPLICATION_COMMUNICATION", "name": "Communication", "type": "APPLICATION"},
    {"key": "APPLICATION_FINANCE", "name": "Finance", "type": "APPLICATION"},
    {"key": "APPLICATION_SHOPPING", "name": "Shopping", "type": "APPLICATION"},
    {"key": "APPLICATION_TOOLS", "name": "Tools", "type": "APPLICATION"},
    {"key": "APPLICATION_EDUCATION", "name": "Education", "type": "APPLICATION"},
    {"key": "APPLICATION_HEALTH_AND_FITNESS", "name": "Health And Fitness", "type": "APPLICATION"},
    {"key": "APPLICATION_LIFESTYLE", "name": "Lifestyle", "type": "APPLICATION"},
    {"key": "APPLICATION_PHOTOGRAPHY", "name": "Photography", "type": "APPLICATION"},
    {"key": "APPLICATION_TRAVEL_AND_LOCAL", "name": "Travel And Local", "type": "APPLICATION"},
    {"key": "APPLICATION_MUSIC_AND_AUDIO", "name": "Music And Audio", "type": "APPLICATION"},
    {"key": "APPLICATION_VIDEO_PLAYERS", "name": "Video Players", "type": "APPLICATION"},
    {"key": "APPLICATION_NEWS_AND_MAGAZINES", "name": "News And Magazines", "type": "APPLICATION"},
    {"key": "APPLICATION_WEATHER", "name": "Weather", "type": "APPLICATION"},
    {"key": "APPLICATION_BOOKS_AND_REFERENCE", "name": "Books And Reference", "type": "APPLICATION"},
    {"key": "APPLICATION_FOOD_AND_DRINK", "name": "Food And Drink", "type": "APPLICATION"},
    {"key": "GAME_ACTION", "name": "Action", "type": "GAME"},
    {"key": "GAME_ADVENTURE", "name": "Adventure", "type": "GAME"},
    {"key": "GAME_ARCADE", "name": "Arcade", "type": "GAME"},
    {"key": "GAME_BOARD", "name": "Board", "type": "GAME"},
    {"key": "GAME_CARD", "name": "Card", "type": "GAME"},
    {"key": "GAME_CASINO", "name": "Casino", "type": "GAME"},
    {"key": "GAME_CASUAL", "name": "Casual", "type": "GAME"},
    {"key": "GAME_EDUCATIONAL", "name": "Educational", "type": "GAME"},
    {"key": "GAME_MUSIC", "name": "Music", "type": "GAME"},
    {"key": "GAME_PUZZLE", "name": "Puzzle", "type": "GAME"},
    {"key": "GAME_RACING", "name": "Racing", "type": "GAME"},
    {"key": "GAME_ROLE_PLAYING", "name": "Role Playing", "type": "GAME"},
    {"key": "GAME_SIMULATION", "name": "Simulation", "type": "GAME"},
    {"key": "GAME_SPORTS", "name": "Sports", "type": "GAME"},
    {"key": "GAME_STRATEGY", "name": "Strategy", "type": "GAME"},
    {"key": "GAME_TRIVIA", "name": "Trivia", "type": "GAME"},
    {"key": "GAME_WORD", "name": "Word", "type": "GAME"},
]


def _get_category_map():
    """카테고리 매핑 생성 (동적으로)"""
    if not SCRAPER_AVAILABLE or not Category:
        return {}
    
    try:
        return {
            "GAME": Category.GAME,
            "APPLICATION": Category.APPLICATION,
            "GAME_ACTION": Category.GAME_ACTION,
            "GAME_ADVENTURE": Category.GAME_ADVENTURE,
            "GAME_ARCADE": Category.GAME_ARCADE,
            "GAME_BOARD": Category.GAME_BOARD,
            "GAME_CARD": Category.GAME_CARD,
            "GAME_CASINO": Category.GAME_CASINO,
            "GAME_CASUAL": Category.GAME_CASUAL,
            "GAME_EDUCATIONAL": Category.GAME_EDUCATIONAL,
            "GAME_MUSIC": Category.GAME_MUSIC,
            "GAME_PUZZLE": Category.GAME_PUZZLE,
            "GAME_RACING": Category.GAME_RACING,
            "GAME_ROLE_PLAYING": Category.GAME_ROLE_PLAYING,
            "GAME_SIMULATION": Category.GAME_SIMULATION,
            "GAME_SPORTS": Category.GAME_SPORTS,
            "GAME_STRATEGY": Category.GAME_STRATEGY,
            "GAME_TRIVIA": Category.GAME_TRIVIA,
            "GAME_WORD": Category.GAME_WORD,
            "APPLICATION_ART_AND_DESIGN": getattr(Category, 'APPLICATION_ART_AND_DESIGN', None),
            "APPLICATION_AUTO_AND_VEHICLES": getattr(Category, 'APPLICATION_AUTO_AND_VEHICLES', None),
            "APPLICATION_BEAUTY": getattr(Category, 'APPLICATION_BEAUTY', None),
            "APPLICATION_BOOKS_AND_REFERENCE": getattr(Category, 'APPLICATION_BOOKS_AND_REFERENCE', None),
            "APPLICATION_BUSINESS": getattr(Category, 'APPLICATION_BUSINESS', None),
            "APPLICATION_COMICS": getattr(Category, 'APPLICATION_COMICS', None),
            "APPLICATION_COMMUNICATION": getattr(Category, 'APPLICATION_COMMUNICATION', None),
            "APPLICATION_DATING": getattr(Category, 'APPLICATION_DATING', None),
            "APPLICATION_EDUCATION": getattr(Category, 'APPLICATION_EDUCATION', None),
            "APPLICATION_ENTERTAINMENT": getattr(Category, 'APPLICATION_ENTERTAINMENT', None),
            "APPLICATION_EVENTS": getattr(Category, 'APPLICATION_EVENTS', None),
            "APPLICATION_FINANCE": getattr(Category, 'APPLICATION_FINANCE', None),
            "APPLICATION_FOOD_AND_DRINK": getattr(Category, 'APPLICATION_FOOD_AND_DRINK', None),
            "APPLICATION_HEALTH_AND_FITNESS": getattr(Category, 'APPLICATION_HEALTH_AND_FITNESS', None),
            "APPLICATION_HOUSE_AND_HOME": getattr(Category, 'APPLICATION_HOUSE_AND_HOME', None),
            "APPLICATION_LIBRARIES_AND_DEMO": getattr(Category, 'APPLICATION_LIBRARIES_AND_DEMO', None),
            "APPLICATION_LIFESTYLE": getattr(Category, 'APPLICATION_LIFESTYLE', None),
            "APPLICATION_MAPS_AND_NAVIGATION": getattr(Category, 'APPLICATION_MAPS_AND_NAVIGATION', None),
            "APPLICATION_MEDICAL": getattr(Category, 'APPLICATION_MEDICAL', None),
            "APPLICATION_NEWS_AND_MAGAZINES": getattr(Category, 'APPLICATION_NEWS_AND_MAGAZINES', None),
            "APPLICATION_PARENTING": getattr(Category, 'APPLICATION_PARENTING', None),
            "APPLICATION_PERSONALIZATION": getattr(Category, 'APPLICATION_PERSONALIZATION', None),
            "APPLICATION_PHOTOGRAPHY": getattr(Category, 'APPLICATION_PHOTOGRAPHY', None),
            "APPLICATION_PRODUCTIVITY": getattr(Category, 'APPLICATION_PRODUCTIVITY', None),
            "APPLICATION_SHOPPING": getattr(Category, 'APPLICATION_SHOPPING', None),
            "APPLICATION_SOCIAL": getattr(Category, 'APPLICATION_SOCIAL', None),
            "APPLICATION_SPORTS": getattr(Category, 'APPLICATION_SPORTS', None),
            "APPLICATION_TOOLS": getattr(Category, 'APPLICATION_TOOLS', None),
            "APPLICATION_TRAVEL_AND_LOCAL": getattr(Category, 'APPLICATION_TRAVEL_AND_LOCAL', None),
            "APPLICATION_VIDEO_PLAYERS": getattr(Category, 'APPLICATION_VIDEO_PLAYERS', None),
            "APPLICATION_WEATHER": getattr(Category, 'APPLICATION_WEATHER', None),
        }
    except Exception as e:
        logger.error(f"Error creating category map: {e}")
        return {}


def get_category_list() -> List[Dict[str, str]]:
    """사용 가능한 카테고리 목록 반환"""
    # google-play-scraper가 설치되어 있지 않으면 기본 목록 반환
    if not SCRAPER_AVAILABLE or not Category:
        logger.info("google-play-scraper not available, returning default categories")
        return DEFAULT_CATEGORIES
    
    # 라이브러리가 있으면 동적으로 생성
    try:
        category_map = _get_category_map()
        if category_map:
            categories = []
            for key in category_map.keys():
                if category_map[key] is not None:  # None인 항목 제외
                    categories.append({
                        "key": key,
                        "name": key.replace("_", " ").title(),
                        "type": "GAME" if key.startswith("GAME") else "APPLICATION"
                    })
            return categories
    except Exception as e:
        logger.error(f"Error getting category list: {e}")
    
    # 에러 발생 시 기본 목록 반환
    return DEFAULT_CATEGORIES


async def fetch_top_apps_real(
    category: str = "top_free",
    limit: int = 100,
    play_category: Optional[str] = None,
    country: str = "kr",
    lang: str = "ko"
) -> List[Dict]:
    """
    Google Play Store에서 상위 앱 목록 가져오기 (실제 구현)
    
    Args:
        category: 순위 타입 ("top_free", "top_paid", "top_grossing")
        limit: 가져올 앱 수 (최대 250)
        play_category: Play Store 카테고리 (예: "APPLICATION", "GAME", "APPLICATION_SOCIAL" 등)
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
        
        # 카테고리 선택
        category_map = _get_category_map()
        play_category_obj = Category.APPLICATION  # 기본값
        if play_category:
            play_category_obj = category_map.get(play_category.upper(), Category.APPLICATION)
        
        # 상위 앱 가져오기
        logger.info(f"Fetching {category} apps from Play Store (category: {play_category}, limit: {limit})...")
        try:
            apps_data = collections(
                collection=collection_type,
                category=play_category_obj,
                results=min(limit, 250),  # 최대 250개까지 가능
                lang=lang,
                country=country
            )
        except Exception as e:
            logger.error(f"Error fetching apps with category {play_category_obj}: {e}")
            # 카테고리 없이 전체 앱 목록 시도
            logger.info("Trying to fetch apps without specific category...")
            apps_data = collections(
                collection=collection_type,
                category=Category.APPLICATION,  # 기본 APPLICATION 카테고리 사용
                results=min(limit * 2, 250),  # 더 많이 가져오기
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
                    "category": app_info.get('genre', play_category or ''),
                    "rating": float(app_info.get('score', 0.0)),
                    "review_count": review_count,
                    "price_model": determine_price_model(app_info),
                    "description": app_info.get('description', ''),
                    "last_update": app_info.get('updated', datetime.now()).isoformat() if isinstance(app_info.get('updated'), datetime) else datetime.now().isoformat(),
                    "icon": app_info.get('icon', ''),
                    "developer": app_info.get('developer', ''),
                    "play_category": play_category or "APPLICATION",  # 추가
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
            "last_update": datetime.now().isoformat(),
            "play_category": "APPLICATION_VIDEO_PLAYERS"
        },
        {
            "name": "Instagram",
            "package_name": "com.instagram.android",
            "category": "Social",
            "rating": 4.5,
            "review_count": 30000000,
            "price_model": "free",
            "description": "사진 및 동영상 공유 소셜 네트워크",
            "last_update": datetime.now().isoformat(),
            "play_category": "APPLICATION_SOCIAL"
        },
    ]
    return sample_apps[:limit]
