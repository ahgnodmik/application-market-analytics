"""
시장성 신호 평가 로직
시장성 점수 항목 (각 0~2점, 최대 10점)
"""


def calculate_marketability_score(
    review_count: int = 0,
    rating: float = 0.0,
    last_update: str = None,
    price_model: str = None,
    description: str = ""
) -> float:
    """
    시장성 점수 계산 (최대 10점)
    
    항목:
    1. 리뷰 수 10만 이상 (2점), 1만 이상 (1점)
    2. 평점 4.2 이상 (2점), 4.0 이상 (1점)
    3. 최근 6개월 내 업데이트 (2점), 1년 내 (1점)
    4. 유료 또는 구독 모델 존재 (2점)
    5. 반복 사용 키워드 포함 (2점): daily, habit, routine, reminder
    """
    score = 0.0
    
    # 1. 리뷰 수
    if review_count >= 100000:
        score += 2.0
    elif review_count >= 10000:
        score += 1.0
    
    # 2. 평점
    if rating >= 4.2:
        score += 2.0
    elif rating >= 4.0:
        score += 1.0
    
    # 3. 최근 업데이트 (6개월 내)
    if last_update:
        try:
            from datetime import datetime, timedelta
            if isinstance(last_update, str):
                update_date = datetime.fromisoformat(last_update.replace('Z', '+00:00'))
            else:
                update_date = last_update
            
            now = datetime.utcnow()
            if isinstance(update_date, datetime):
                if update_date.tzinfo:
                    now = datetime.now(update_date.tzinfo)
                delta = now - update_date
                
                if delta.days <= 180:  # 6개월
                    score += 2.0
                elif delta.days <= 365:  # 1년
                    score += 1.0
        except:
            pass
    
    # 4. 유료/구독 모델
    if price_model and price_model.lower() in ['paid', 'subscription']:
        score += 2.0
    
    # 5. 반복 사용 키워드
    desc_lower = description.lower() if description else ""
    repeat_keywords = ['daily', 'habit', 'routine', 'reminder', 'tracker', 'track']
    if any(keyword in desc_lower for keyword in repeat_keywords):
        score += 2.0
    
    return min(score, 10.0)  # 최대 10점


def parse_date(date_str):
    """날짜 문자열 파싱"""
    if not date_str:
        return None
    
    from datetime import datetime
    try:
        # ISO 형식
        if 'T' in date_str:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        # 기타 형식
        formats = ['%Y-%m-%d', '%Y/%m/%d', '%m/%d/%Y']
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except:
                continue
    except:
        pass
    
    return None




