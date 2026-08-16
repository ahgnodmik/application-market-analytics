# Application Market Analytics — 프로젝트 아카이브

> **아카이빙: 2026-08-16.** 이 저장소는 개발 종료 후 아카이빙됨.
> 로컬 폴더에는 이 문서와 `.git`만 남김. 전체 소스는 git 히스토리(원격 HEAD)에 보존.
> 복원: `git clone https://github.com/ahgnodmik/application-market-analytics.git`
> 또는 이 폴더에서 `git checkout <아카이빙 커밋> -- .`

## 개요

안드로이드 Play Store 상위 앱을 분석해 **구현 난이도가 낮고 시장성이 검증된 앱 타입**을 추출하는 내부용 분석 서비스.

- 앱 데이터 입력 + CSV 업로드
- 기능 단위 분해 및 관리
- 구현 난이도 자동 계산 (0~2점)
- 시장성 신호 점수 자동 계산 (0~10점)
- 2축 매트릭스 시각화 (난이도 × 시장성)
- 앱 타입 그룹화 및 추천
- Play Store 데이터 자동 수집 (매주 월요일 스케줄러)
- Notion 스타일 UI (Tailwind CSS)

## 기술 스택

- **백엔드**: Python 3.10, FastAPI 0.104.1, Uvicorn 0.24.0, SQLAlchemy 2.0.23, Pydantic 2.5.0
- **데이터**: pandas 2.1.3, google-play-scraper 1.2.5, beautifulsoup4 4.12.2 + lxml
- **AI**: OpenAI 1.3.0 (GPT 카테고리 분석)
- **프론트**: Jinja2 템플릿 + Tailwind CSS 3.4.19 (Node ≥18로 빌드)
- **DB**: SQLite (로컬 dev) / PostgreSQL (프로덕션, psycopg2-binary)
- **배포**: Railway (nixpacks)

## 아키텍처

```
app/
├── main.py                 # FastAPI 진입점, 페이지 라우트 + /health
├── config.py               # Settings — .env → .env.local 순 로드, dev/prod 분리
├── database.py             # SQLAlchemy 엔진/세션 (SQLite↔PostgreSQL 자동 선택)
├── models.py               # ORM 모델 (아래 스키마 참조)
├── schemas.py              # Pydantic 요청/응답 스키마
├── worker.py               # 스케줄러 워커 프로세스
├── routers/
│   ├── apps.py             # 앱 CRUD (GET /api/apps/)
│   ├── analysis.py         # 추천/매트릭스 (GET /api/analysis/*)
│   ├── upload.py           # CSV 업로드
│   └── playstore.py        # 순위 수집 (POST /api/playstore/fetch-rankings)
├── tasks/scheduler.py      # 매주 월요일 실행, ScheduledTask로 중복 실행 방지
└── services/
    ├── play_store_scraper.py       # Play Store 수집 (구버전/래퍼)
    ├── play_store_scraper_real.py  # 실제 google-play-scraper 기반 수집
    ├── difficulty_scorer.py        # 난이도 점수
    ├── marketability_scorer.py     # 시장성 점수
    ├── category_analyzer.py        # GPT 카테고리 분석
    ├── type_grouper.py             # 앱 타입 그룹화
    ├── openai_service.py           # OpenAI API 래퍼
    └── pipeline.py                 # scrape → normalize → score → store

templates/  # base, dashboard(메인+수집 UI), apps, analysis(매트릭스), category_analysis
static/     # input.css(Tailwind 소스) → style.css(빌드), apps.js, analysis.js
```

## API 엔드포인트

- 페이지: `GET /`(대시보드), `/apps`, `/analysis`, `/category-analysis`
- `GET /health` — DB·OpenAI 상태 포함 헬스체크
- `GET /api/apps/` — 앱 목록
- `GET /api/analysis/recommendations` — 조건 필터 앱 타입 추천
- `GET /api/analysis/matrix` — 2축 매트릭스 데이터
- `POST /api/playstore/fetch-rankings` — Play Store 수집 (월요일만, `force=true`로 강제)

## DB 스키마 (models.py)

- **App**: id, name, package_name(UNIQUE), category, rating, review_count, price_model(free/paid/subscription), difficulty_score(0~2), marketability_score(0~10), features(1:N), rankings(1:N)
- **Feature**: id, app_id(FK), name, feature_type(input/storage/query/notification/media), difficulty_score
- **AppType**: id, name(UNIQUE), core_features(JSON), mvp_screens, build_time, avg_difficulty, avg_marketability, app_count
- **ScheduledTask**: id, task_name, task_date(YYYY-WW), status(pending/running/completed/failed), result_data(JSON) — 주간 중복 실행 방지
- **AppRanking**: id, app_id(FK), rank, category, rank_change, previous_rank, fetched_at

## 핵심 비즈니스 로직

**난이도 점수 (difficulty_scorer.py)** — 기능별 0~2:
- 0점: CRUD, 리스트, 로컬 저장, 단순 알림
- 1점: 로그인, API 연동, 결제, 오디오/비디오 재생
- 2점: 실시간 처리, AI, 대규모 동기화, 복잡한 그래픽

**시장성 점수 (marketability_scorer.py)** — 5개 항목 각 0~2, 총 0~10:
1. 리뷰 수: 10만+ = 2, 1만+ = 1
2. 평점: 4.2+ = 2, 4.0+ = 1
3. 최근 업데이트: 6개월 내 = 2, 1년 내 = 1
4. 유료/구독 모델 = 2
5. 반복 사용 키워드 = 2

**추천 필터**: 시장성 ≥ 6 AND 난이도 ≤ 1.0 AND 핵심 기능 ≤ 5

## 배포 (Railway)

- `Procfile`: `web: python3 -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- `nixpacks.toml`: python310 + pip install requirements.txt
- `package.json` postinstall: `tailwindcss -i ./static/input.css -o ./static/style.css --minify`
- 스케줄러: 매주 월요일 Play Store 자동 수집, `SCHEDULER_ENABLED`로 제어

## 환경변수 (이름만 — 값은 Railway 대시보드/로컬 관리)

- `DATABASE_URL` — PostgreSQL 연결 (Railway 자동 주입, 없으면 SQLite)
- `PORT` — Railway 자동 주입
- `OPENAI_API_KEY` — GPT 분석 (선택)
- `APP_ENV` — `dev`(기본) / `prod`
- `LOG_LEVEL` — `INFO`(기본) / `DEBUG`
- `SCHEDULER_ENABLED` — 기본 `true`

## 의존성 전문

### requirements.txt
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
pandas==2.1.3
python-multipart==0.0.6
jinja2==3.1.2
aiofiles==23.2.1
openai==1.3.0
python-dotenv==1.0.0
httpx==0.25.0
mangum==0.17.0
psycopg2-binary==2.9.9
beautifulsoup4==4.12.2
lxml==4.9.3
google-play-scraper==1.2.5
```

### package.json (핵심)
```json
{
  "scripts": {
    "dev": "python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000",
    "start": "python3 -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}",
    "build:css": "tailwindcss -i ./static/input.css -o ./static/style.css --minify",
    "postinstall": "npm run build:css"
  },
  "engines": { "python": "3.10", "node": ">=18.0.0" },
  "devDependencies": {
    "autoprefixer": "^10.4.23",
    "postcss": "^8.5.6",
    "tailwindcss": "^3.4.19"
  }
}
```

## 최근 작업 맥락 (아카이빙 시점)

Play Store 실제 데이터 수집 안정화에 집중:
- 샘플 데이터 대신 실제 Play Store 수집으로 전환, 샘플 감지 + 재시도 로직
- YouTube/Instagram 등 초대형 앱 제외, 저난이도 앱만 수집
- 전체 필터링 시 fetch limit 증가 + 재시도
- 수집 실패 시 큐레이션 폴백 (다양한 샘플 앱, YouTube/Instagram 제외)
- 미커밋 검증 스크립트 2개 최종 커밋에 포함: `check_collection_analysis.py`(DB 상태 확인), `test_collection_api.py`(Railway 배포 테스트)

## 재실행 절차

```bash
git clone https://github.com/ahgnodmik/application-market-analytics.git
cd application-market-analytics
python3 -m pip install -r requirements.txt
npm install                # Tailwind CSS 자동 빌드 (postinstall)
cp .env.example .env       # OPENAI_API_KEY 채우기 (선택)
npm run dev                # http://localhost:8000
```

## 미보존 항목

- `market_analytics.db` (로컬 SQLite, 82KB 수집 데이터) — gitignore 대상이라 git에 없음. 스케줄러/수집 API로 재수집 가능
- `.env.local` (시크릿) — 삭제됨, 값은 별도 관리
- `node_modules/`, 빌드 산출물 — `npm install`로 재생성
