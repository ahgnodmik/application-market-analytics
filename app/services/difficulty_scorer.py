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




