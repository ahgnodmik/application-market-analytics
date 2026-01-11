# 🔧 Google Play Store 실제 파싱 구현 가이드

## 방법 1: google-play-scraper 라이브러리 사용 (권장) ✅

가장 간단하고 안정적인 방법입니다.

### 설치

```bash
pip install google-play-scraper
```

### 사용 예시

```python
from google_play_scraper import collections, Collection, Category

# 상위 무료 앱 가져오기
top_free = collections(
    collection=Collection.TOP_FREE,
    category=Category.APPLICATION,
    results=100,
    lang='ko',
    country='kr'
)

for app in top_free:
    print(app['title'])      # 앱 이름
    print(app['appId'])      # 패키지 이름
    print(app['score'])      # 평점
    print(app['installs'])   # 설치 수
    print(app['description']) # 설명
```

### 구현된 파일

- `app/services/play_store_scraper_real.py`: 실제 구현
- `app/services/play_store_scraper.py`: 래퍼 (자동으로 실제 구현 사용)

### 장점

- ✅ 간단한 API
- ✅ 안정적
- ✅ 유지보수 필요 없음
- ✅ 공식 API와 유사한 데이터 제공

---

## 방법 2: 직접 HTML 스크래핑

BeautifulSoup을 사용하여 직접 파싱 (더 복잡하지만 더 세밀한 제어 가능)

### 구현 방법

```python
from bs4 import BeautifulSoup
import httpx

async def fetch_play_store_html(category: str):
    url = f"https://play.google.com/store/apps/collection/topselling_free"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Play Store HTML 구조에 따라 파싱
        app_cards = soup.find_all('div', class_='...')
        
        for card in app_cards:
            # 앱 정보 추출
            name = card.find('a', {'title': True}).get('title')
            # ...
```

### 주의사항

- ⚠️ Play Store HTML 구조 변경 시 수정 필요
- ⚠️ Rate limiting 가능성
- ⚠️ User-Agent 설정 필요
- ⚠️ 더 복잡한 구현

---

## 방법 3: 서드파티 API 사용

AppBrain, AppAnnie 등의 서드파티 API 사용

### 장점

- ✅ 더 안정적
- ✅ 더 많은 데이터
- ✅ API 키만으로 사용 가능

### 단점

- ❌ 유료일 수 있음
- ❌ API 키 필요
- ❌ 외부 서비스 의존

---

## 현재 구현 상태

### ✅ 구현 완료

1. **google-play-scraper 통합**
   - `app/services/play_store_scraper_real.py`: 실제 구현
   - `requirements.txt`: google-play-scraper 추가
   - 자동 fallback 시스템

2. **래퍼 시스템**
   - `play_store_scraper.py`에서 자동으로 실제 구현 사용
   - 라이브러리가 없으면 샘플 데이터 사용

### 📝 사용 방법

#### 1. 의존성 설치

```bash
pip install -r requirements.txt
# 또는
pip install google-play-scraper
```

#### 2. 코드 사용

```python
from app.services.play_store_scraper import fetch_top_apps

# 자동으로 실제 구현 사용 (google-play-scraper)
apps = await fetch_top_apps(category="top_free", limit=100)
```

#### 3. API 사용

```bash
# 월요일이 아니면 에러
curl -X POST "https://app-analytics.up.railway.app/api/playstore/fetch-rankings"

# 강제 실행
curl -X POST "https://app-analytics.up.railway.app/api/playstore/fetch-rankings?force=true"
```

---

## 다음 단계

### 1. Railway 배포 후 테스트

1. Railway가 자동으로 재배포
2. 의존성 설치 확인 (`google-play-scraper`)
3. API 테스트: `/api/playstore/fetch-rankings?force=true`

### 2. 실제 데이터 확인

```bash
# 상태 확인
curl "https://app-analytics.up.railway.app/api/playstore/status"

# 강제 실행 (실제 데이터 가져오기)
curl -X POST "https://app-analytics.up.railway.app/api/playstore/fetch-rankings?force=true&limit=10"
```

### 3. 데이터 검증

- 앱 이름이 실제 Play Store 앱인지 확인
- 평점, 리뷰 수가 실제 데이터인지 확인
- 패키지 이름이 올바른지 확인

---

## 문제 해결

### google-play-scraper 설치 실패

```bash
# Python 버전 확인 (3.7 이상 필요)
python3 --version

# pip 업그레이드
pip install --upgrade pip

# 재설치
pip install google-play-scraper
```

### 라이브러리 작동 안함

- 현재는 샘플 데이터 사용 (fallback)
- 로그 확인: `play_store_scraper_real.py`에서 에러 메시지 확인

### Rate Limiting

- google-play-scraper는 자체적으로 rate limiting 처리
- 너무 많은 요청 시 에러 발생 가능
- 적절한 딜레이 추가 고려

---

## 참고 자료

- [google-play-scraper GitHub](https://github.com/JoMingyu/google-play-scraper)
- [Google Play Store](https://play.google.com/store/apps)
