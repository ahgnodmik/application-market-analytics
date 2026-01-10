# 🚀 빠른 시작 가이드

## 기획서 기반 서비스 작동 방법

### 1️⃣ 기본 워크플로우

```
1. 앱 데이터 입력 (수동 또는 CSV 업로드)
   ↓
2. 기능 분해 및 난이도 자동 계산
   ↓
3. 시장성 점수 자동 계산
   ↓
4. 필터링 조건 설정 (기획서 기본값)
   - 시장성 점수 ≥ 6.0
   - 구현 난이도 ≤ 1.0
   - 핵심 기능 수 ≤ 5
   ↓
5. 추천 앱 타입 목록 확인
   - 타입 이름
   - 핵심 기능 3~5개
   - 예상 화면 수
   - 예상 구현 기간
```

---

## 2️⃣ 사용 방법

### 방법 1: 웹 인터페이스 사용

1. **대시보드 접속**
   ```
   https://app-market-analytics.netlify.app/
   ```

2. **앱 추가**
   - "앱 관리" 메뉴 클릭
   - "앱 추가" 버튼 클릭
   - 필수 정보 입력:
     - 앱 이름
     - 카테고리
     - 평점 (Rating)
     - 리뷰 수 (Review Count)
     - 가격 모델 (free/paid/subscription)
     - 최근 업데이트 날짜
     - 앱 설명

3. **기능 추가**
   - 앱 상세 페이지에서 "기능 추가" 버튼 클릭
   - 기능 이름, 설명, 타입 입력
   - 난이도 점수는 자동 계산됨 (0~2점)

4. **분석 및 추천 확인**
   - "분석" 메뉴 클릭
   - 필터 조건 확인 (기획서 기본값)
   - 추천 앱 타입 목록 확인

### 방법 2: CSV 업로드 (대량 입력)

1. **CSV 파일 준비**
   ```
   name,category,rating,review_count,price_model,last_update,description
   "할일 관리 앱","Productivity",4.5,150000,"free","2024-01-01","매일 사용하는 할일 관리"
   ```

2. **업로드**
   - "앱 관리" → "CSV 업로드" 버튼 클릭
   - CSV 파일 선택 및 업로드

---

## 3️⃣ API 사용 (프로그래밍 방식)

### 앱 생성
```bash
curl -X POST "https://app-market-analytics.netlify.app/api/apps/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "할일 관리 앱",
    "category": "Productivity",
    "rating": 4.5,
    "review_count": 150000,
    "price_model": "free",
    "description": "매일 사용하는 할일 관리 앱"
  }'
```

### 기능 추가
```bash
curl -X POST "https://app-market-analytics.netlify.app/api/apps/1/features" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "항목 추가",
    "description": "새로운 할일 항목을 추가하는 기능",
    "feature_type": "input"
  }'
```

### 추천 앱 타입 조회
```bash
curl "https://app-market-analytics.netlify.app/api/analysis/recommendations?min_marketability=6&max_difficulty=1.0&max_features=5"
```

---

## 4️⃣ 필터링 조건 (기획서 기준)

### 기본 필터 조건
- **시장성 점수**: ≥ 6.0 (최대 10점)
- **구현 난이도**: ≤ 1.0 (0~2점)
- **핵심 기능 수**: ≤ 5개

### 시장성 점수 계산 항목 (각 0~2점)
1. 리뷰 수: 10만 이상 (2점), 1만 이상 (1점)
2. 평점: 4.2 이상 (2점), 4.0 이상 (1점)
3. 최근 업데이트: 6개월 내 (2점), 1년 내 (1점)
4. 유료/구독 모델: 존재 (2점)
5. 반복 사용 키워드: daily, habit, routine, reminder 포함 (2점)

### 난이도 점수 기준
- **0점**: CRUD, 리스트, 로컬 저장, 단순 알림
- **1점**: 로그인, API 연동, 결제, 오디오/비디오 재생
- **2점**: 실시간 처리, AI, 대규모 동기화, 복잡한 그래픽

---

## 5️⃣ 예상 결과

### 추천 앱 타입 정보
각 추천 타입은 다음 정보를 포함합니다:

- **타입 이름**: 예) "체크리스트/할일 관리"
- **핵심 기능**: 예) ["항목 추가", "항목 체크", "날짜 저장"]
- **예상 화면 수**: 예) 3개
- **예상 구현 기간**: 예) "2주일 이내"
- **평균 난이도**: 예) 0.5
- **평균 시장성**: 예) 7.5
- **포함 앱 수**: 예) 5개

---

## 6️⃣ 문제 해결

### 웹페이지가 보이지 않는 경우
1. Health Check 확인: `https://app-market-analytics.netlify.app/health`
2. Functions 로그 확인: Netlify 대시보드 → Functions → server → Logs
3. 브라우저 개발자 도구 콘솔 확인

### 데이터가 저장되지 않는 경우
- Netlify Functions는 SQLite를 `/tmp` 디렉토리에 저장 (임시)
- 프로덕션 환경에서는 외부 DB 권장 (Supabase, MongoDB Atlas)

### 추천 항목이 없는 경우
1. 필터 조건 완화 시도
2. 앱 데이터 확인 (시장성 점수, 난이도 점수)
3. 기능 수 확인 (5개 이하)

---

## 7️⃣ 성공 판단 기준 (기획서)

> 상위 100 앱 분석 후 **구현 가능 앱 타입 10개 이상 도출**, 각 타입당 MVP 정의가 1페이지 이내로 가능

### 확인 방법
1. 최소 10개 이상의 앱 데이터 입력
2. 각 앱에 3~5개의 기능 추가
3. 필터 조건 확인 (기획서 기본값)
4. 추천 앱 타입 목록에서 10개 이상 확인

---

## 8️⃣ 다음 단계

1. **샘플 데이터 입력**
   - Play Store 상위 앱 데이터 수집
   - CSV로 대량 업로드

2. **분석 실행**
   - 필터 조건 확인
   - 추천 앱 타입 확인

3. **결과 활용**
   - 추천된 앱 타입 중 선택
   - MVP 정의 문서 작성 (1페이지)
   - 개발 시작!

---

## 📚 추가 리소스

- **서비스 검증 문서**: `SERVICE_VERIFICATION.md`
- **API 문서**: `https://app-market-analytics.netlify.app/docs` (FastAPI 자동 생성)
- **배포 가이드**: `NETLIFY_DEPLOY.md`
