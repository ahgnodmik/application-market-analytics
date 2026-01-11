# 📊 Application Market Analytics - 현재 상태 요약 리포트

**생성일**: 2024년 1월  
**버전**: 1.0.0  
**플랫폼**: Railway (Python FastAPI)

---

## 🎯 프로젝트 개요

Android Play Store 상위 앱을 분석하여, 구현 난이도가 낮으면서 시장성이 검증된 앱 타입을 추천하는 서비스입니다.

**핵심 목표**: "1인 개발자가 빠르게 구축 가능하며 실패 확률이 낮은 앱 구조" 도출

---

## ✅ 구현 완료 기능

### 1. Google Play Store 앱 순위 수집

- **주기**: 매주 월요일 GMT+9 기준 자동 수집
- **방법**: `google-play-scraper` 라이브러리 사용
- **데이터**: 상위 100개 앱 (무료/유료/수익순)
- **카테고리별 수집**: 37개 이상의 Play Store 카테고리 지원

**주요 파일**:
- `app/services/play_store_scraper_real.py`: 실제 파싱 구현
- `app/routers/playstore.py`: API 엔드포인트
- `app/tasks/scheduler.py`: 주기적 실행 로직

**API 엔드포인트**:
- `POST /api/playstore/fetch-rankings`: 앱 순위 가져오기
- `POST /api/playstore/fetch-by-category`: 카테고리별 순위 가져오기
- `GET /api/playstore/categories`: 사용 가능한 카테고리 목록
- `GET /api/playstore/status`: 수집 상태 확인

---

### 2. 카테고리별 GPT 분석

- **단일 카테고리 분석**: 특정 카테고리의 상위 앱을 GPT로 분석
- **다중 카테고리 비교 분석**: 여러 카테고리를 비교하여 인사이트 제공
- **분석 내용**:
  - 카테고리 특성 및 트렌드
  - 성공 패턴 분석
  - 시장 기회 분석
  - 추천 앱 아이디어 (구현 난이도, 시장성 점수 포함)

**주요 파일**:
- `app/services/category_analyzer.py`: GPT 분석 로직
- `templates/category_analysis.html`: UI 페이지

**API 엔드포인트**:
- `POST /api/playstore/analyze-category`: 카테고리별 분석
- `POST /api/playstore/analyze-multiple-categories`: 다중 카테고리 비교 분석

---

### 3. 앱 분석 및 추천 시스템

- **시장성 점수 계산**: 리뷰 수, 평점, 가격 모델 등 기반
- **난이도 점수 계산**: 기능 타입 및 복잡도 기반
- **앱 타입 그룹화**: 유사한 기능 조합을 가진 앱들을 그룹화
- **추천 시스템**: 시장성 ≥ 6.0, 난이도 ≤ 1.0, 기능 수 ≤ 5개 조건 필터링

**주요 파일**:
- `app/services/marketability_scorer.py`: 시장성 점수 계산
- `app/services/difficulty_scorer.py`: 난이도 점수 계산
- `app/services/type_grouper.py`: 앱 타입 그룹화
- `app/routers/analysis.py`: 분석 API

**API 엔드포인트**:
- `GET /api/analysis/recommendations`: 추천 앱 타입 목록
- `GET /api/analysis/matrix`: 2축 매트릭스 데이터 (난이도 vs 시장성)
- `GET /api/analysis/types`: 모든 앱 타입 목록

---

### 4. 웹 UI

- **대시보드**: 주요 통계 및 추천 앱 타입 표시
- **앱 목록**: Play Store에서 가져온 앱 목록 조회
- **분석 페이지**: 2축 매트릭스 및 추천 시스템
- **카테고리 분석**: 카테고리별 GPT 분석 인터페이스
- **AI 리포트**: 전체 앱 데이터 기반 GPT 리포트 생성

**주요 파일**:
- `templates/dashboard.html`: 대시보드
- `templates/apps.html`: 앱 목록
- `templates/analysis.html`: 분석 페이지
- `templates/category_analysis.html`: 카테고리 분석
- `templates/report.html`: AI 리포트
- `static/apps.js`, `static/analysis.js`: JavaScript 로직

---

### 5. 데이터베이스

- **SQLite** (로컬 개발) / **PostgreSQL** (Railway 배포)
- **주요 테이블**:
  - `apps`: 앱 정보 (package_name으로 Play Store 앱 식별)
  - `features`: 앱 기능 목록
  - `app_types`: 추천 앱 타입

**주요 파일**:
- `app/models.py`: 데이터베이스 모델
- `app/database.py`: 데이터베이스 연결 설정

---

## 📁 프로젝트 구조

```
016-Application-market-analytics/
├── app/
│   ├── main.py                 # FastAPI 앱 진입점
│   ├── database.py             # DB 연결 설정
│   ├── models.py               # DB 모델
│   ├── schemas.py              # Pydantic 스키마
│   ├── routers/
│   │   ├── apps.py             # 앱 관리 API
│   │   ├── analysis.py         # 분석 API
│   │   ├── playstore.py        # Play Store 수집 API
│   │   ├── report.py           # 리포트 API
│   │   └── upload.py           # CSV 업로드 API
│   ├── services/
│   │   ├── play_store_scraper.py           # Play Store 스크래퍼 (래퍼)
│   │   ├── play_store_scraper_real.py      # 실제 파싱 구현
│   │   ├── category_analyzer.py            # 카테고리 GPT 분석
│   │   ├── marketability_scorer.py         # 시장성 점수 계산
│   │   ├── difficulty_scorer.py            # 난이도 점수 계산
│   │   ├── type_grouper.py                 # 앱 타입 그룹화
│   │   └── openai_service.py               # OpenAI API 서비스
│   └── tasks/
│       └── scheduler.py        # 주기적 작업 스케줄러
├── templates/                  # HTML 템플릿
├── static/                     # 정적 파일 (CSS, JS)
├── requirements.txt            # Python 의존성
├── Procfile                    # Railway 시작 명령
├── nixpacks.toml              # Railway 빌드 설정
└── runtime.txt                # Python 버전
```

---

## 🔌 주요 API 엔드포인트

### Play Store 수집
- `POST /api/playstore/fetch-rankings` - 앱 순위 가져오기
- `POST /api/playstore/fetch-by-category` - 카테고리별 수집
- `GET /api/playstore/categories` - 카테고리 목록
- `GET /api/playstore/status` - 수집 상태 확인
- `POST /api/playstore/analyze-category` - 카테고리 GPT 분석
- `POST /api/playstore/analyze-multiple-categories` - 다중 카테고리 비교 분석

### 앱 관리
- `GET /api/apps/playstore` - Play Store 앱 목록 조회
- `GET /api/apps/{id}` - 앱 상세 조회

### 분석
- `GET /api/analysis/recommendations` - 추천 앱 타입
- `GET /api/analysis/matrix` - 2축 매트릭스 데이터
- `GET /api/analysis/types` - 앱 타입 목록

### 리포트
- `POST /api/report/generate` - AI 리포트 생성

---

## 🎨 웹 페이지

- `/` - 대시보드
- `/apps` - Play Store 앱 목록
- `/analysis` - 분석 페이지 (매트릭스 + 추천)
- `/category-analysis` - 카테고리 분석 페이지
- `/report` - AI 리포트 생성 페이지

---

## 📦 주요 의존성

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
openai==1.3.0
google-play-scraper==1.2.5
beautifulsoup4==4.12.2
httpx==0.25.0
psycopg2-binary==2.9.9  # PostgreSQL 지원
```

---

## 🚀 배포 환경

- **플랫폼**: Railway
- **Python 버전**: 3.10
- **데이터베이스**: PostgreSQL (Railway)
- **시작 명령**: `python3 -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`

---

## 🔑 환경 변수

- `OPENAI_API_KEY`: OpenAI API 키 (GPT 분석용)
- `PORT`: 서버 포트 (Railway에서 자동 설정)
- `DATABASE_URL`: PostgreSQL 연결 문자열 (Railway에서 자동 설정)

---

## 📊 현재 데이터 구조

### App 모델
- `id`: 고유 ID
- `name`: 앱 이름
- `package_name`: Play Store 패키지 이름 (Play Store 앱 식별용)
- `category`: 카테고리
- `rating`: 평점
- `review_count`: 리뷰 수
- `price_model`: 가격 모델 (free/paid/subscription)
- `description`: 설명
- `difficulty_score`: 난이도 점수 (0-2)
- `marketability_score`: 시장성 점수 (0-10)

### Feature 모델
- `id`: 고유 ID
- `app_id`: 앱 ID (외래키)
- `name`: 기능 이름
- `feature_type`: 기능 타입 (input/storage/query/notification/media)
- `difficulty_score`: 난이도 점수

### AppType 모델
- `id`: 고유 ID
- `name`: 앱 타입 이름
- `core_features`: 핵심 기능 리스트 (JSON)
- `mvp_screens`: 예상 화면 수
- `build_time`: 예상 개발 기간
- `avg_difficulty`: 평균 난이도
- `avg_marketability`: 평균 시장성
- `app_count`: 해당 타입 앱 수

---

## 🔄 주기적 작업

- **매주 월요일 GMT+9**: Play Store 상위 앱 자동 수집
- **실행 위치**: FastAPI startup event에서 자동 확인 및 실행

---

## ⚠️ 제한사항 및 주의사항

1. **분석 기능 제한**: 
   - 추천 시스템은 기능(features)이 추가된 앱에 대해서만 작동
   - Play Store에서 가져온 앱은 기본적으로 기능이 없음

2. **데이터 수집**:
   - `google-play-scraper` 라이브러리가 없을 경우 샘플 데이터 사용
   - 실제 데이터 수집을 위해서는 라이브러리 설치 필요

3. **OpenAI API**:
   - GPT 분석 기능 사용 시 API 키 필요
   - API 키 없을 경우 분석 기능 사용 불가

---

## 🎯 주요 사용 시나리오

### 1. 주간 자동 수집
- 매주 월요일 GMT+9에 자동으로 Play Store 상위 앱 수집
- 카테고리별로 수집 가능

### 2. 카테고리 분석
1. `/category-analysis` 페이지 접속
2. 카테고리 선택
3. GPT 분석 실행
4. 분석 결과 확인 (트렌드, 성공 패턴, 추천 아이디어)

### 3. 앱 타입 추천
1. Play Store에서 앱 수집
2. 앱에 기능 추가 (선택사항)
3. `/analysis` 페이지에서 추천 확인
4. 필터 조건 조정하여 원하는 앱 타입 찾기

### 4. AI 리포트 생성
1. `/report` 페이지 접속
2. 분석할 앱 선택 (또는 전체)
3. GPT 리포트 생성
4. 마크다운 형식 리포트 확인

---

## 📈 다음 단계 제안

1. **기능 개선**:
   - Play Store 앱 자동 기능 추출 (GPT 또는 규칙 기반)
   - 앱 타입별 상세 분석 페이지
   - 히스토리 추적 (순위 변동 등)

2. **성능 최적화**:
   - 데이터베이스 인덱싱 최적화
   - 캐싱 전략 구현
   - 배치 처리 최적화

3. **UI/UX 개선**:
   - 반응형 디자인 개선
   - 차트 라이브러리 사용 (Chart.js 등)
   - 로딩 상태 개선

4. **모니터링**:
   - 로깅 시스템 강화
   - 에러 추적
   - 성능 모니터링

---

## 📝 최근 변경사항

### 2024년 1월
- ✅ Play Store 카테고리별 수집 기능 추가
- ✅ 카테고리별 GPT 분석 기능 추가
- ✅ 대시보드, 앱 목록, 분석 기능을 Play Store 앱 전용으로 변경
- ✅ 대시보드에서 "총 앱 수" 카드 제거
- ✅ 분석 API 에러 처리 개선
- ✅ 프론트엔드 null safety 추가

---

## 📞 기술 지원

- **프레임워크**: FastAPI
- **데이터베이스**: SQLAlchemy ORM
- **프론트엔드**: Tailwind CSS, Vanilla JavaScript
- **배포**: Railway
- **버전 관리**: Git/GitHub

---

**문서 버전**: 1.0  
**최종 업데이트**: 2024년 1월
