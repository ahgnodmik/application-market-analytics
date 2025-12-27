"""
앱 타입 그룹화 로직
유사한 핵심 기능 조합을 가진 앱들을 그룹화
"""

from typing import List, Dict
from collections import defaultdict
from app.models import App, Feature


def group_apps_by_type(apps: List[App]) -> Dict[str, List[App]]:
    """
    앱들을 기능 조합 기준으로 그룹화
    """
    groups = defaultdict(list)
    
    for app in apps:
        # 핵심 기능 이름들을 정렬하여 키로 사용
        feature_names = sorted([f.name.lower() for f in app.features])
        key = "_".join(feature_names[:5])  # 최대 5개 기능만 사용
        
        if not key:
            key = "unknown"
        
        groups[key].append(app)
    
    return dict(groups)


def generate_type_name(features: List[str]) -> str:
    """
    기능 리스트로부터 앱 타입 이름 생성
    """
    if not features:
        return "기타"
    
    # 주요 기능 키워드 추출
    main_feature = features[0].title() if features else ""
    
    # 일반적인 앱 타입 패턴 매칭
    feature_lower = " ".join(features).lower()
    
    if any(kw in feature_lower for kw in ['check', 'list', 'todo']):
        return "체크리스트/할일 관리"
    elif any(kw in feature_lower for kw in ['habit', 'track', 'routine']):
        return "습관 추적"
    elif any(kw in feature_lower for kw in ['note', 'memo', 'write']):
        return "메모/노트"
    elif any(kw in feature_lower for kw in ['timer', 'clock', 'alarm']):
        return "타이머/알람"
    elif any(kw in feature_lower for kw in ['calculator', 'calc']):
        return "계산기"
    elif any(kw in feature_lower for kw in ['converter', 'convert']):
        return "변환기"
    elif any(kw in feature_lower for kw in ['qr', 'barcode', 'scan']):
        return "QR/바코드 스캔"
    elif any(kw in feature_lower for kw in ['weather']):
        return "날씨"
    elif any(kw in feature_lower for kw in ['password', 'vault']):
        return "비밀번호 관리"
    elif any(kw in feature_lower for kw in ['calendar', 'schedule']):
        return "캘린더/스케줄"
    else:
        return f"{main_feature} 앱"


def estimate_build_time(feature_count: int, difficulty_score: float) -> str:
    """
    예상 구현 기간 추정
    """
    base_days = feature_count * 2  # 기능당 기본 2일
    
    if difficulty_score >= 1.5:
        multiplier = 2.0
    elif difficulty_score >= 1.0:
        multiplier = 1.5
    else:
        multiplier = 1.0
    
    total_days = int(base_days * multiplier)
    
    if total_days <= 7:
        return "1주일 이내"
    elif total_days <= 14:
        return "2주일 이내"
    elif total_days <= 30:
        return "1개월 이내"
    else:
        return "1개월 이상"


def estimate_mvp_screens(feature_count: int) -> int:
    """
    예상 MVP 화면 수 추정
    """
    # 기본 화면: 메인, 상세
    base_screens = 2
    
    # 기능 타입별 추가 화면
    additional = max(0, feature_count - 2) // 2
    
    return base_screens + additional




