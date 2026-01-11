# 디버깅 가이드

## 현재 발생하는 문제

1. **카테고리 분석 500 에러**
2. **앱 수집이 Instagram/YouTube만 나옴**

## 문제 진단

### 1. Railway 로그 확인

Railway 대시보드에서 다음을 확인하세요:

1. Railway 대시보드 접속
2. 프로젝트 선택
3. "Deployments" 탭 → 최신 배포 선택
4. "View Logs" 클릭
5. 다음 메시지들을 찾아보세요:

#### OpenAI API 관련
- `OpenAI API key not found` → API 키 미설정
- `OpenAI client is None` → API 키 설정 오류
- `Error code: 401` → API 키가 유효하지 않음
- `Error code: 429` → API 사용량 한도 초과

#### Play Store 스크래퍼 관련
- `google-play-scraper not installed, using fallback` → 라이브러리 미설치
- `google-play-scraper not available, cannot fetch real data` → 라이브러리 사용 불가
- `Only sample apps returned` → 샘플 데이터 사용 중
- `Error fetching Play Store data` → 스크래퍼 오류

### 2. 환경 변수 확인

Railway 대시보드 → Variables 탭에서 확인:

- `OPENAI_API_KEY`: 설정되어 있는가? (sk-로 시작하는가?)
- `DATABASE_URL`: PostgreSQL 연결 문자열이 올바른가?

### 3. 라이브러리 설치 확인

`requirements.txt`에 다음이 포함되어 있는지 확인:

```
google-play-scraper==1.2.5
openai==1.3.0
```

Railway 로그에서 다음을 확인:

```
Installing required dependencies from requirements.txt
Successfully installed google-play-scraper-1.2.5
```

## 해결 방법

### 1. OpenAI API 키 설정

1. Railway 대시보드 → Variables 탭
2. `OPENAI_API_KEY` 추가 또는 수정
3. 값: 실제 OpenAI API 키 (https://platform.openai.com/api-keys)
4. 저장 후 자동 재배포 대기

### 2. google-play-scraper 확인

라이브러리가 설치되어 있어도 작동하지 않을 수 있습니다:

- Railway 로그에서 실제 오류 메시지 확인
- Rate limiting으로 인한 차단 가능성
- Play Store API 변경 가능성

### 3. 임시 해결책

현재는 샘플 데이터(YouTube, Instagram)만 사용 중일 수 있습니다. 
이는 정상적인 fallback 동작입니다.

## 로그 예시

### 정상 작동
```
[INFO] Using google-play-scraper for top_free apps, play_category: APPLICATION_SOCIAL, limit: 50
[INFO] Fetching top_free apps from Play Store (category: APPLICATION_SOCIAL, limit: 50)...
[INFO] Successfully fetched 50 apps from Play Store
[INFO] Fetched 50 apps
[INFO] GPT analysis result: success=True
```

### 문제 발생
```
[WARNING] google-play-scraper not installed, using fallback
[ERROR] Error fetching apps: ...
[WARNING] Only sample apps returned (likely google-play-scraper not working). Apps: ['YouTube', 'Instagram']
[ERROR] OpenAI client is None - API key may not be set
```

## 추가 확인 사항

1. **Railway 빌드 로그**: 패키지 설치가 성공했는지 확인
2. **런타임 로그**: 애플리케이션 시작 시 오류 확인
3. **API 응답**: 브라우저 개발자 도구에서 실제 에러 메시지 확인
