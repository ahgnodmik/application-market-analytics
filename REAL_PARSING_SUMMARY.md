# ✅ 실제 Play Store 파싱 구현 완료

## 구현 방법

### 방법 1: google-play-scraper 라이브러리 사용 (권장) ✅

가장 간단하고 안정적인 방법입니다.

#### 설치

```bash
pip install google-play-scraper
```

또는

```bash
pip install -r requirements.txt
```

#### 구현 파일

- `app/services/play_store_scraper_real.py`: 실제 구현
- `app/services/play_store_scraper.py`: 래퍼 (자동으로 실제 구현 사용)

#### 작동 방식

1. **google-play-scraper 사용 시도**
   - 라이브러리가 설치되어 있으면 실제 데이터 가져오기
   - 한국 Play Store 상위 앱 가져오기

2. **Fallback 시스템**
   - 라이브러리가 없으면 HTML 스크래핑 시도
   - HTML 스크래핑 실패 시 샘플 데이터 사용

## 사용 방법

### API로 테스트

```bash
# 강제 실행 (실제 데이터 가져오기)
curl -X POST "https://app-analytics.up.railway.app/api/playstore/fetch-rankings?force=true&limit=10"

# 상태 확인
curl "https://app-analytics.up.railway.app/api/playstore/status"
```

### 자동 실행

- 매주 월요일 GMT+9 기준으로 자동 실행
- FastAPI startup event에서 확인
- 또는 Railway cron job 설정

## 다음 단계

### 1. Railway 배포

Railway가 자동으로 재배포합니다. 배포 후:

1. 의존성 설치 확인:
   - `google-play-scraper` 자동 설치됨
   - `requirements.txt`에 포함됨

2. API 테스트:
   ```bash
   curl -X POST "https://app-analytics.up.railway.app/api/playstore/fetch-rankings?force=true&limit=5"
   ```

3. 실제 데이터 확인:
   - 앱 이름이 실제 Play Store 앱인지 확인
   - 평점, 리뷰 수가 실제 데이터인지 확인
   - 패키지 이름이 올바른지 확인

### 2. 데이터 검증

가져온 데이터 확인:
- 한국 Play Store 상위 앱인지
- 실제 평점과 일치하는지
- 패키지 이름이 올바른지

### 3. 문제 해결

#### google-play-scraper 설치 실패

Railway 로그 확인:
- 의존성 설치 로그 확인
- 에러 메시지 확인

#### 데이터가 샘플 데이터인 경우

- 라이브러리가 제대로 설치되지 않았을 수 있음
- 로그에서 "Using sample data as fallback" 메시지 확인
- `requirements.txt`에 `google-play-scraper` 확인

## 예상 결과

### 성공 시

```json
{
  "success": true,
  "message": "100개 앱 가져오기 완료",
  "saved_count": 95,
  "updated_count": 5,
  "skipped_count": 0,
  "category": "top_free",
  "fetched_at": "2024-01-15T09:00:00+09:00"
}
```

### 실제 데이터 예시

```json
{
  "name": "카카오톡",
  "package_name": "com.kakao.talk",
  "category": "Communication",
  "rating": 4.5,
  "review_count": 10000000,
  "price_model": "free",
  "description": "무료 메시징 앱",
  "last_update": "2024-01-10T00:00:00"
}
```

## 참고

- [google-play-scraper GitHub](https://github.com/JoMingyu/google-play-scraper)
- [IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md): 상세 구현 가이드
- [PLAY_STORE_PARSING_GUIDE.md](./PLAY_STORE_PARSING_GUIDE.md): 파싱 가이드
