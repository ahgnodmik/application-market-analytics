# 📱 Google Play Store 자동 순위 수집 기능

## 기능 개요

매주 월요일 **GMT+9 (KST)** 기준으로 Google Play Store에서 상위 앱 순위를 자동으로 가져옵니다.

## 구현 내용

### 1. Play Store 스크래퍼 (`app/services/play_store_scraper.py`)

- Google Play Store에서 앱 순위 데이터 가져오기
- 월요일인지 확인하는 함수
- HTML 파싱 (BeautifulSoup 사용)

### 2. Play Store API (`app/routers/playstore.py`)

**엔드포인트:**

- `POST /api/playstore/fetch-rankings`
  - 앱 순위 가져오기
  - 매개변수:
    - `category`: "top_free", "top_paid", "top_grossing"
    - `limit`: 가져올 앱 수 (최대 100)
    - `force`: 월요일이 아니어도 강제로 가져오기

- `GET /api/playstore/status`
  - 현재 상태 확인
  - 현재 요일, 가져올 수 있는지 확인

- `GET /api/playstore/last-fetch`
  - 마지막으로 가져온 시간 확인
  - 다음 예정된 시간 확인

### 3. 자동 스케줄러 (`app/tasks/scheduler.py`)

- 매주 월요일 자동 실행
- FastAPI startup event에서 확인
- Railway cron job으로도 실행 가능

### 4. 데이터베이스 모델 업데이트

- `App` 모델에 `package_name` 필드 추가
- 패키지 이름 기준으로 중복 확인

## 작동 방식

### 자동 실행

1. **FastAPI 시작 시 확인**
   - 앱이 시작될 때 월요일이면 자동으로 순위 가져오기
   - 백그라운드에서 실행 (앱 시작을 블로킹하지 않음)

2. **수동 실행**
   - API 엔드포인트 호출: `POST /api/playstore/fetch-rankings`
   - `force=true`로 설정하면 언제든지 실행 가능

### 시간 기준

- **기준 시간대**: GMT+9 (Asia/Seoul)
- **실행 요일**: 매주 월요일
- **확인 방법**: `should_fetch_this_week()` 함수

## 사용 방법

### 1. API로 수동 실행

```bash
# 월요일이 아니면 에러
curl -X POST "https://app-analytics.up.railway.app/api/playstore/fetch-rankings"

# 강제 실행 (언제든지)
curl -X POST "https://app-analytics.up.railway.app/api/playstore/fetch-rankings?force=true"
```

### 2. 상태 확인

```bash
# 현재 상태 확인
curl "https://app-analytics.up.railway.app/api/playstore/status"

# 마지막 가져온 시간 확인
curl "https://app-analytics.up.railway.app/api/playstore/last-fetch"
```

### 3. 자동 실행 (월요일)

- 앱이 시작될 때 월요일이면 자동으로 실행
- 또는 Railway cron job 설정 (선택사항)

## Railway Cron Job 설정 (선택사항)

Railway에서 주기적으로 실행하려면:

1. Railway 대시보드 → 프로젝트 설정
2. Cron Jobs 추가
3. 스케줄: `0 9 * * 1` (매주 월요일 오전 9시 KST = UTC+9)

또는 별도 스크립트 생성:
```python
# cron_task.py
import asyncio
from app.tasks.scheduler import check_and_fetch_rankings

asyncio.run(check_and_fetch_rankings())
```

## 데이터 처리

1. **중복 확인**: 패키지 이름 기준
2. **기존 앱**: 업데이트 (평점, 리뷰 수 등)
3. **신규 앱**: 생성
4. **시장성 점수**: 자동 재계산

## 주의사항

1. **Play Store 크롤링**
   - 현재는 샘플 데이터 사용 (실제 구현 필요)
   - BeautifulSoup을 사용한 HTML 파싱
   - 또는 서드파티 API 사용 고려

2. **Rate Limiting**
   - Play Store는 크롤링을 제한할 수 있음
   - 적절한 딜레이 및 User-Agent 설정 필요

3. **에러 처리**
   - 크롤링 실패 시 샘플 데이터 사용 (개발 단계)
   - 프로덕션에서는 에러 로깅 및 알림 필요

## 다음 단계

1. **실제 Play Store 크롤링 구현**
   - BeautifulSoup으로 HTML 파싱
   - 또는 서드파티 API 사용 (AppBrain, AppAnnie 등)

2. **Railway Cron Job 설정**
   - 매주 월요일 자동 실행
   - 또는 FastAPI startup event 사용

3. **에러 처리 개선**
   - 실패 시 재시도 로직
   - 알림 시스템 (이메일, Slack 등)
