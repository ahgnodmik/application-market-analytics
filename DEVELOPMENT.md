# 🛠️ 개발 가이드

## 로컬 개발 환경

### 1. 의존성 설치

```bash
# Python 의존성 설치
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env.local` 파일 생성 (또는 `.env`):

```bash
OPENAI_API_KEY=your-api-key-here
```

### 3. 로컬 서버 실행

#### 방법 1: npm 스크립트 사용 (권장)

```bash
npm run dev
```

서버가 http://localhost:8000 에서 실행됩니다.

#### 방법 2: Python 직접 실행

```bash
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 방법 3: 실행 스크립트 사용

```bash
chmod +x run.sh
./run.sh
```

### 4. 브라우저에서 접속

- **대시보드**: http://localhost:8000
- **앱 관리**: http://localhost:8000/apps
- **분석**: http://localhost:8000/analysis
- **AI 리포트**: http://localhost:8000/report
- **API 문서**: http://localhost:8000/docs

---

## Railway 배포

Railway에 배포되어 있습니다.

자세한 배포 가이드는 `RAILWAY_DEPLOY.md` 및 `RAILWAY_QUICK_START.md`를 참고하세요.

---

## 사용 가능한 npm 스크립트

| 명령어 | 설명 |
|--------|------|
| `npm run dev` | 로컬 개발 서버 실행 (포트 8000) |
| `npm start` | 프로덕션 서버 실행 |

---

## 환경 변수

### 로컬 개발

`.env.local` 또는 `.env` 파일:

```env
OPENAI_API_KEY=your-api-key-here
DATABASE_URL=sqlite:///./market_analytics.db
```

### Railway 배포

Railway 대시보드 → Variables:

- `OPENAI_API_KEY`: OpenAI API 키
- `DATABASE_URL`: (자동 설정 - PostgreSQL)

---

## 데이터베이스

### 로컬 개발

- 기본: SQLite (`market_analytics.db`)
- 파일이 자동으로 생성됩니다

### Railway 배포

- PostgreSQL 자동 제공
- `DATABASE_URL` 환경 변수 자동 설정

---

## 문제 해결

### 포트가 이미 사용 중인 경우

```bash
# 다른 포트 사용
python3 -m uvicorn app.main:app --reload --port 8001
```

### 모듈을 찾을 수 없는 경우

```bash
pip install -r requirements.txt
```

---

## 프로젝트 구조

```
application-market-analytics/
├── app/                    # FastAPI 애플리케이션
│   ├── main.py            # 메인 앱
│   ├── routers/           # API 라우터
│   ├── services/          # 비즈니스 로직
│   ├── models.py          # 데이터베이스 모델
│   ├── config.py          # 설정 관리
│   └── worker.py          # 워커 프로세스
├── templates/             # HTML 템플릿
├── static/                # 정적 파일 (CSS, JS)
├── requirements.txt       # Python 의존성
├── Procfile               # Railway 시작 명령
├── nixpacks.toml         # Railway 빌드 설정
├── runtime.txt           # Python 버전
└── package.json           # npm 스크립트
```
