"""
구현 난이도 평가 로직
기능별 난이도 점수 (0~2)
"""


def calculate_feature_difficulty(feature_type: str, description: str = "") -> float:
    """
    기능별 난이도 점수 계산 (0~2)
    
    0: CRUD, 리스트, 로컬 저장, 단순 알림
    1: 로그인, API 연동, 결제, 오디오/비디오 재생
    2: 실시간 처리, AI, 대규모 동기화, 복잡한 그래픽
    """
    desc_lower = description.lower() if description else ""
    
    # 점수 2: 고난이도
    if any(keyword in desc_lower for keyword in [
        'ai', 'artificial intelligence', 'machine learning', 'ml',
        'real-time', 'realtime', 'real time', 'sync', 'synchronization',
        'complex graphics', '3d', 'rendering', 'animation',
        'blockchain', 'cryptocurrency', 'crypto'
    ]):
        return 2.0
    
    # 점수 1: 중간 난이도
    if any(keyword in desc_lower for keyword in [
        'login', 'authentication', 'auth', 'sign in', 'sign up',
        'api', 'api integration', 'rest', 'graphql',
        'payment', 'purchase', 'subscription', 'billing',
        'audio', 'video', 'playback', 'streaming', 'media player'
    ]):
        return 1.0
    
    # 기능 타입별 기본 점수
    if feature_type == "media":
        return 1.0
    elif feature_type in ["input", "storage", "query"]:
        return 0.0
    elif feature_type == "notification":
        return 0.0
    
    # 기본값: 단순 기능
    return 0.0


def calculate_app_difficulty(feature_scores: list[float]) -> float:
    """
    앱 구현 난이도 = 모든 기능 난이도 평균
    """
    if not feature_scores:
        return 0.0
    
    return sum(feature_scores) / len(feature_scores)


def estimate_difficulty_from_description(description: str) -> float:
    """
    앱 설명을 기반으로 난이도 추정 (기능이 없을 때 사용)
    
    Returns:
        0.0 ~ 2.0 사이의 난이도 점수
    """
    if not description:
        return 0.0
    
    desc_lower = description.lower()
    
    # 고난이도 키워드 (2.0)
    high_difficulty_keywords = [
        'ai', 'artificial intelligence', 'machine learning', 'ml', 'deep learning',
        'real-time', 'realtime', 'real time', 'live', 'streaming',
        'blockchain', 'cryptocurrency', 'crypto', 'nft',
        '3d', 'vr', 'ar', 'virtual reality', 'augmented reality',
        'complex', 'advanced', 'enterprise', 'enterprise-grade'
    ]
    
    # 중간 난이도 키워드 (1.0)
    medium_difficulty_keywords = [
        'api', 'integration', 'sync', 'synchronization', 'cloud',
        'payment', 'purchase', 'subscription', 'billing', 'in-app purchase',
        'social', 'login', 'authentication', 'auth', 'sign in',
        'video', 'audio', 'media', 'playback', 'recording',
        'database', 'server', 'backend', 'rest', 'graphql'
    ]
    
    # 단순 기능 키워드 (0.0)
    simple_keywords = [
        'note', 'memo', 'todo', 'list', 'reminder', 'calendar',
        'calculator', 'converter', 'timer', 'stopwatch',
        'simple', 'easy', 'basic', 'lightweight', 'minimal'
    ]
    
    # 키워드 매칭
    high_count = sum(1 for keyword in high_difficulty_keywords if keyword in desc_lower)
    medium_count = sum(1 for keyword in medium_difficulty_keywords if keyword in desc_lower)
    simple_count = sum(1 for keyword in simple_keywords if keyword in desc_lower)
    
    # 점수 계산
    if high_count > 0:
        return min(2.0, 1.5 + (high_count * 0.1))
    elif medium_count > 0:
        return min(1.5, 0.5 + (medium_count * 0.15))
    elif simple_count > 0:
        return 0.0
    else:
        # 키워드가 없으면 설명 길이와 복잡도로 추정
        word_count = len(description.split())
        if word_count > 100:
            return 1.0  # 긴 설명은 중간 난이도
        elif word_count > 50:
            return 0.5
        else:
            return 0.0





