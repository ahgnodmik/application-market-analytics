# 📊 Application Market Analytics - 현재 상태 요약 리포트

**생성일**: 2024년 1월  
**버전**: 1.0.0  
**플랫폼**: Railway (Python FastAPI)  
**기획서 버전**: 최종 (섹션 1-18)

---

## 🎯 프로젝트 개요

### 목적

Android Play Store 상위 100개 앱을 분석하여, **구현 난이도가 매우 낮고 시장성이 검증된 신호를 가진** 앱 **타입(Type)**을 빠르게 추출하는 내부용 분석 서비스입니다.

**핵심 목표**: "지금 당장 혼자서 빠르게 만들 수 있으면서도 실패 확률이 낮은 앱 구조" 도출

### 사용 대상

- 1인 개발자 / 디자이너
- MVP 중심의 사이드 프로젝트 제작자
- 빠른 시장 검증이 필요한 기획자

### 핵심 원칙

- ✅ 정밀 분석보다 **속도와 일관성** 우선
- ✅ 모든 판단은 **숫자화된 규칙**으로 처리
- ✅ 앱이 아닌 **기능 단위 / 앱 타입 단위**로 분석

---

## 📋 전체 시스템 구조 (기획서 기준)

```
[Play Store 상위 100 앱 데이터]
        ↓
[기능 단위 분해]
        ↓
[구현 난이도 점수 계산]
        ↓
[시장성 신호 점수 계산]
        ↓
[2축 매트릭스 필터링]
        ↓
[빠른 구현 + 시장성 앱 타입 목록]
```

**현재 구현 상태**: ✅ 전체 파이프라인 구현 완료

---

## ✅ 구현 완료 기능

### 1. Google Play Store 앱 순위 수집 ✅

**기획 요구사항**:
- Google Play Store 카테고리별 상위 앱 중 Top 100
- 매주 월요일 GMT+9 기준 자동 수집

**구현 상태**:
- ✅ `google-play-scraper` 라이브러리 사용
- ✅ 37개 이상의 Play Store 카테고리 지원
- ✅ 주간 자동 수집 스케줄러 구현 (매주 월요일 GMT+9)
- ✅ 카테고리별 수집 기능
- ✅ 수동 수집 (force 옵션) 지원

**주요 파일**:
- `app/services/play_store_scraper_real.py`: 실제 파싱 구현
- `app/routers/playstore.py`: API 엔드포인트
- `app/tasks/scheduler.py`: 주기적 실행 로직

**API 엔드포인트**:
- `POST /api/playstore/fetch-rankings`: 앱 순위 가져오기
- `POST /api/playstore/fetch-by-category`: 카테고리별 순위 가져오기
- `GET /api/playstore/categories`: 사용 가능한 카테고리 목록 (37개+)
- `GET /api/playstore/status`: 수집 상태 확인
- `GET /api/playstore/last-fetch`: 마지막 수집 시간 확인

---

### 2. 기능 단위 분해 모델 ✅

**기획 요구사항**:
- 화면 또는 사용자 행동 기준으로 분해
- 하나의 기능 = 하나의 주요 사용자 액션
- 기능 유형 태그: 입력/저장/조회/알림/미디어

**구현 상태**:
- ✅ Feature 모델 구현
- ✅ 기능 타입 분류 지원 (input/storage/query/notification/media)
- ✅ 앱별 기능 목록 관리
- ⚠️ **제한사항**: 현재는 수동 입력만 지원 (자동 분해 미구현)

**데이터베이스 모델**:
```python
Feature:
  - id: 고유 ID
  - app_id: 앱 ID (외래키)
  - name: 기능 이름
  - feature_type: 기능 타입 (input/storage/query/notification/media)
  - difficulty_score: 난이도 점수 (0-2)
```

---

### 3. 구현 난이도 평가 로직 ✅

**기획 요구사항** (섹션 5.1):

| 점수 | 기준                           |
| -- | ---------------------------- |
| 0  | CRUD, 리스트, 로컬 저장, 단순 알림      |
| 1  | 로그인, API 연동, 결제, 오디오/비디오 재생  |
| 2  | 실시간 처리, AI, 대규모 동기화, 복잡한 그래픽 |

**계산 방식**: `앱 구현 난이도 = 모든 기능 난이도 평균`

**구현 상태**:
- ✅ 기능별 난이도 점수 계산 로직 구현
- ✅ 앱 전체 난이도 점수 계산 (기능 평균)
- ✅ `app/services/difficulty_scorer.py`에 구현

**주요 파일**:
- `app/services/difficulty_scorer.py`: 난이도 점수 계산 로직

---

### 4. 시장성 신호 평가 로직 ✅

**기획 요구사항** (섹션 6.1):
시장성 점수 항목 (각 0~2점):
1. 리뷰 수 10만 이상
2. 평점 4.2 이상
3. 최근 6개월 내 업데이트
4. 유료 또는 구독 모델 존재
5. 반복 사용 키워드 포함 (daily, habit, routine, reminder)

**계산 방식**: `시장성 점수 = 항목별 점수 합계 (최대 10점)`

**구현 상태**:
- ✅ 시장성 점수 계산 로직 구현
- ✅ 5개 항목 모두 평가
- ✅ `app/services/marketability_scorer.py`에 구현

**주요 파일**:
- `app/services/marketability_scorer.py`: 시장성 점수 계산 로직

---

### 5. 2축 매트릭스 필터링 ✅

**기획 요구사항** (섹션 7):
- X축: 구현 난이도 (낮을수록 우수)
- Y축: 시장성 점수 (높을수록 우수)

**후보 추출 조건**:
```
시장성 점수 ≥ 6
AND 구현 난이도 ≤ 1.0
AND 핵심 기능 수 ≤ 5
```

**구현 상태**:
- ✅ 2축 매트릭스 데이터 API 구현
- ✅ 필터 조건 적용 가능
- ✅ `/analysis` 페이지에서 시각화
- ✅ 추천 시스템에 조건 적용

**API 엔드포인트**:
- `GET /api/analysis/matrix`: 매트릭스 데이터
- `GET /api/analysis/recommendations`: 필터 조건 적용 추천

---

### 6. 앱 타입(Type) 그룹화 ✅

**기획 요구사항** (섹션 8):
- 유사한 핵심 기능 조합 기준으로 그룹화
- 동일한 사용자 행동 패턴 기준

**출력 정보**:
- Type Name (앱 타입 이름)
- Core Features (핵심 기능 3~5개)
- MVP Screens (예상 화면 수)
- Build Time (예상 구현 기간)
- Notes (차별화 포인트) - 선택사항

**구현 상태**:
- ✅ 앱 타입 그룹화 로직 구현
- ✅ 타입 이름 자동 생성
- ✅ MVP 화면 수 및 개발 기간 추정
- ✅ AppType 모델로 저장

**주요 파일**:
- `app/services/type_grouper.py`: 그룹화 및 타입 이름 생성 로직

---

### 7. 카테고리별 GPT 분석 ✅ (확장 기능)

**기획 요구사항**: 원본에는 없으나, 확장 아이디어로 추가 구현

**구현 상태**:
- ✅ 단일 카테고리 분석
- ✅ 다중 카테고리 비교 분석
- ✅ GPT를 통한 트렌드 및 패턴 분석
- ✅ 시장 기회 분석

**주요 파일**:
- `app/services/category_analyzer.py`: GPT 분석 로직
- `templates/category_analysis.html`: UI 페이지

**API 엔드포인트**:
- `POST /api/playstore/analyze-category`: 카테고리별 분석
- `POST /api/playstore/analyze-multiple-categories`: 다중 카테고리 비교 분석

---

### 8. 웹 UI ✅

**기획 요구사항** (섹션 9.2):
1. 대시보드 ✅
2. 앱 상세 분석 화면 ✅ (앱 목록 페이지)
3. 매트릭스 뷰 ✅
4. 후보 앱 타입 리스트 ✅

**추가 구현**:
- 카테고리 분석 페이지 (확장)
- AI 리포트 페이지 (확장)

**구현 상태**:
- ✅ Tailwind CSS 기반 Notion 스타일 UI
- ✅ 반응형 디자인
- ✅ 모든 필수 페이지 구현

**주요 파일**:
- `templates/dashboard.html`: 대시보드
- `templates/apps.html`: 앱 목록
- `templates/analysis.html`: 분석 페이지 (매트릭스 + 추천)
- `templates/category_analysis.html`: 카테고리 분석
- `templates/report.html`: AI 리포트

---

## 📁 프로젝트 구조

```
016-Application-market-analytics/
├── app/
│   ├── main.py                 # FastAPI 앱 진입점
│   ├── database.py             # DB 연결 설정 (SQLite/PostgreSQL)
│   ├── models.py               # DB 모델 (App, Feature, AppType)
│   ├── schemas.py              # Pydantic 스키마
│   ├── routers/
│   │   ├── apps.py             # 앱 관리 API
│   │   ├── analysis.py         # 분석 API (매트릭스, 추천)
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
├── templates/                  # HTML 템플릿 (Jinja2)
├── static/                     # 정적 파일 (CSS, JS)
├── requirements.txt            # Python 의존성
├── Procfile                    # Railway 시작 명령
├── nixpacks.toml              # Railway 빌드 설정
└── runtime.txt                # Python 버전 (3.10)
```

---

## 🔌 주요 API 엔드포인트

### Play Store 수집
- `POST /api/playstore/fetch-rankings` - 앱 순위 가져오기
- `POST /api/playstore/fetch-by-category` - 카테고리별 수집
- `GET /api/playstore/categories` - 카테고리 목록 (37개+)
- `GET /api/playstore/status` - 수집 상태 확인
- `GET /api/playstore/last-fetch` - 마지막 수집 시간
- `POST /api/playstore/analyze-category` - 카테고리 GPT 분석
- `POST /api/playstore/analyze-multiple-categories` - 다중 카테고리 비교 분석

### 앱 관리
- `GET /api/apps/playstore` - Play Store 앱 목록 조회
- `GET /api/apps/{id}` - 앱 상세 조회

### 분석
- `GET /api/analysis/recommendations` - 추천 앱 타입 (필터 조건 적용)
- `GET /api/analysis/matrix` - 2축 매트릭스 데이터
- `GET /api/analysis/types` - 앱 타입 목록

### 리포트
- `POST /api/report/generate` - AI 리포트 생성
- `POST /api/report/analyze-app/{app_id}` - 단일 앱 분석

---

## 🎨 웹 페이지

- `/` - 대시보드 (통계, 빠른 작업)
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
python-dotenv==1.0.0
jinja2==3.1.2
pandas==2.1.3
```

---

## 🚀 배포 환경

**플랫폼**: Railway  
**Python 버전**: 3.10  
**데이터베이스**: PostgreSQL (Railway)  
**시작 명령**: `python3 -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`

---

## 🔑 환경 변수

**필수**:
- `OPENAI_API_KEY`: OpenAI API 키 (GPT 분석용)
- `PORT`: 서버 포트 (Railway에서 자동 설정)
- `DATABASE_URL`: PostgreSQL 연결 문자열 (Railway에서 자동 설정)

**선택**:
- `APP_ENV`: `prod` / `dev`
- `LOG_LEVEL`: `INFO` / `DEBUG`
- `SCHEDULER_ENABLED`: `true` / `false`

---

## 📊 데이터베이스 구조

### App 모델
- `id`: 고유 ID
- `name`: 앱 이름
- `package_name`: Play Store 패키지 이름 (Play Store 앱 식별용, UNIQUE)
- `category`: 카테고리
- `rating`: 평점
- `review_count`: 리뷰 수
- `price_model`: 가격 모델 (free/paid/subscription)
- `description`: 설명
- `last_update`: 최근 업데이트 날짜
- `difficulty_score`: 난이도 점수 (0-2)
- `marketability_score`: 시장성 점수 (0-10)
- `created_at`: 생성 시간

### Feature 모델
- `id`: 고유 ID
- `app_id`: 앱 ID (외래키)
- `name`: 기능 이름
- `feature_type`: 기능 타입 (input/storage/query/notification/media)
- `difficulty_score`: 난이도 점수 (0-2)

### AppType 모델
- `id`: 고유 ID
- `name`: 앱 타입 이름
- `core_features`: 핵심 기능 리스트 (JSON)
- `mvp_screens`: 예상 화면 수
- `build_time`: 예상 개발 기간
- `avg_difficulty`: 평균 난이도
- `avg_marketability`: 평균 시장성
- `app_count`: 해당 타입 앱 수
- `notes`: 차별화 포인트 (선택사항)

---

## 🔄 주기적 작업 (스케줄러)

**기획 요구사항** (섹션 14.5):
- 매주 월요일 GMT+9 기준 자동 수집
- 중복 실행 방지 필요

**구현 상태**:
- ✅ FastAPI startup event에서 스케줄러 실행
- ✅ `should_fetch_this_week()` 함수로 주간 중복 방지
- ⚠️ **제한사항**: 현재는 단일 프로세스 방식 (멀티 인스턴스 시 중복 실행 가능)

**권장 개선사항** (기획서 14.5 참고):
- Web/Worker 분리 (Railway 서비스 2개)
- DB 락 또는 작업 테이블로 중복 방지 강화

**주요 파일**:
- `app/tasks/scheduler.py`: 스케줄러 로직
- `app/main.py`: startup event에서 실행

---

## ⚠️ 기획서 대비 구현 상태

### ✅ 완전 구현된 기능

1. ✅ Play Store 앱 순위 수집 (카테고리별)
2. ✅ 기능 단위 분해 모델
3. ✅ 구현 난이도 평가 로직 (기획서 5.1 기준)
4. ✅ 시장성 신호 평가 로직 (기획서 6.1 기준)
5. ✅ 2축 매트릭스 필터링 (기획서 7 기준)
6. ✅ 앱 타입 그룹화 (기획서 8 기준)
7. ✅ 필수 화면 구성 (기획서 9.2 기준)
8. ✅ 웹 배포 (Railway)

### ⚠️ 부분 구현 / 제한사항

1. **기능 자동 분해**: 현재 수동 입력만 지원 (기획서 12 "AI 기반 기능 자동 분해"는 미구현)
2. **스케줄러 중복 방지**: 기본적인 주간 중복 방지는 있으나, 멀티 인스턴스 환경에서 완벽하지 않음
3. **트렌드 변화 비교**: 월별 비교 기능 미구현 (기획서 12)
4. **iOS App Store 확장**: 미구현 (기획서 12)

### ➕ 기획서 외 추가 구현

1. ✅ 카테고리별 GPT 분석 (기획서 12의 "확장 아이디어"를 미리 구현)
2. ✅ AI 리포트 생성 (단일 앱 및 전체 앱 분석)
3. ✅ CSV 업로드 기능 (기획서 3.2 "수동 입력 또는 CSV 업로드" 지원)

---

## 📈 성공 판단 기준 (기획서 11)

**기획 요구사항**:
- 상위 100 앱 분석 후
- **구현 가능 앱 타입 10개 이상 도출**
- 각 타입당 MVP 정의가 1페이지 이내로 가능

**현재 상태**: 
- ✅ 분석 시스템 구축 완료
- ✅ 앱 타입 도출 기능 구현 완료
- ⚠️ 실제 데이터 수집 및 검증 필요

---

## 🎯 주요 사용 시나리오

### 1. 주간 자동 수집
- 매주 월요일 GMT+9에 자동으로 Play Store 상위 앱 수집
- 카테고리별로 수집 가능

### 2. 카테고리 분석
1. `/category-analysis` 페이지 접속
2. 카테고리 선택 (37개+ 카테고리 중 선택)
3. GPT 분석 실행
4. 분석 결과 확인 (트렌드, 성공 패턴, 추천 아이디어)

### 3. 앱 타입 추천
1. Play Store에서 앱 수집
2. 앱에 기능 추가 (수동)
3. `/analysis` 페이지에서 추천 확인
4. 필터 조건 조정 (시장성 ≥ 6, 난이도 ≤ 1.0, 기능 수 ≤ 5)

### 4. AI 리포트 생성
1. `/report` 페이지 접속
2. 분석할 앱 선택 (또는 전체)
3. GPT 리포트 생성
4. 마크다운 형식 리포트 확인

---

## 🔧 배포 체크리스트 (기획서 15)

### ✅ 로컬 사전 확인
- ✅ `pip install -r requirements.txt`
- ✅ `uvicorn app.main:app --reload`로 페이지 정상 로드
- ✅ `/api/playstore/status` 응답 확인
- ✅ `POST /api/playstore/fetch-rankings` 실행 후 DB 저장 확인
- ✅ `/analysis` 페이지에서 매트릭스 데이터 렌더링 확인

### ✅ Railway 배포
- ✅ GitHub 연결
- ✅ Railway New Project → Deploy from GitHub
- ✅ Postgres 추가
- ✅ 환경 변수 설정 (`OPENAI_API_KEY` 등)
- ✅ Start Command/Procfile 확인
- ✅ 배포 후 `/` 대시보드 및 주요 API 호출 확인

### ⚠️ 운영 안전장치 (개선 필요)
- ✅ 스케줄러 기본 중복 방지 (주간 체크)
- ⚠️ 멀티 인스턴스 환경 중복 방지 강화 필요
- ✅ 에러 로깅 (INFO 레벨)
- ✅ OpenAI 호출 실패 시 graceful fallback (에러 처리 구현)

---

## 📝 다음 단계 제안 (기획서 12, 16 참고)

### 단기 개선 (기획서 16.1-16.3)

1. **설정 통합**:
   - `app/config.py` 생성하여 환경 변수 로딩 통합
   - dev/prod 설정 분리

2. **실행 엔트리 분리** (기획서 14.5):
   - `app/main.py`: 웹 (uvicorn)
   - `app/worker.py`: 스케줄러/배치 (선택사항)

3. **데이터 파이프라인 명확화**:
   - `scrape → normalize → store → analyze → recommend` 단계별 함수 분리
   - 단계별 결과 DB 저장 (디버깅/재처리 가능)

### 중장기 확장 (기획서 12)

1. **AI 기반 기능 자동 분해**: GPT를 활용한 자동 기능 추출
2. **트렌드 변화 비교**: 월별 데이터 비교 및 시각화
3. **iOS App Store 확장**: iOS 앱 분석 추가
4. **성능 최적화**: 데이터베이스 인덱싱, 캐싱 전략

---

## 📞 기술 스택

**백엔드**:
- FastAPI (Python 웹 프레임워크)
- SQLAlchemy (ORM)
- PostgreSQL / SQLite

**프론트엔드**:
- Tailwind CSS (스타일링)
- Vanilla JavaScript
- Jinja2 (템플릿)

**외부 서비스**:
- OpenAI API (GPT 분석)
- Google Play Scraper (앱 데이터 수집)

**배포**:
- Railway (호스팅)
- GitHub (버전 관리)

---

## 📝 최근 변경사항

### 2024년 1월
- ✅ Play Store 카테고리별 수집 기능 추가
- ✅ 카테고리별 GPT 분석 기능 추가
- ✅ 대시보드, 앱 목록, 분석 기능을 Play Store 앱 전용으로 변경
- ✅ 대시보드에서 "총 앱 수" 카드 제거
- ✅ 분석 API 에러 처리 개선
- ✅ 프론트엔드 null safety 추가
- ✅ 현재 상태 리포트 생성

---

## 📚 참고 문서

- **기획서**: 프로젝트 루트의 기획 문서 (섹션 1-18)
- **배포 가이드**: 기획서 섹션 14-17
- **API 문서**: `/docs` (Swagger UI)

---

**문서 버전**: 2.0 (기획서 기준 업데이트)  
**최종 업데이트**: 2024년 1월  
**기획서 버전**: 최종 (섹션 1-18)
