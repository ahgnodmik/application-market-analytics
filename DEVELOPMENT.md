# 🛠️ 개발 가이드

## 로컬 개발 환경

### 1. 의존성 설치

```bash
# Python 의존성 설치
pip install -r requirements.txt

# Netlify CLI 설치 (선택사항 - Netlify Functions 로컬 테스트용)
npm install -g netlify-cli
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

## Netlify 배포

### 1. Netlify Functions 로컬 테스트

Netlify 환경을 로컬에서 시뮬레이션:

```bash
npm run netlify:dev
```

또는:

```bash
netlify dev
```

이렇게 하면:
- Netlify Functions가 로컬에서 실행됨
- 환경 변수 자동 로드
- http://localhost:8888 에서 접속 가능

### 2. 배포

#### 미리보기 배포

```bash
npm run netlify:deploy
```

#### 프로덕션 배포

```bash
npm run netlify:deploy:prod
```

### 3. Git 연동 (자동 배포)

Git에 푸시하면 자동으로 배포됩니다:

```bash
git add .
git commit -m "Your commit message"
git push
```

---

## 사용 가능한 npm 스크립트

| 명령어 | 설명 |
|--------|------|
| `npm run dev` | 로컬 개발 서버 실행 (포트 8000) |
| `npm start` | 프로덕션 서버 실행 |
| `npm run netlify:dev` | Netlify Functions 로컬 테스트 |
| `npm run netlify:deploy` | Netlify 미리보기 배포 |
| `npm run netlify:deploy:prod` | Netlify 프로덕션 배포 |

---

## 환경 변수

### 로컬 개발

`.env.local` 또는 `.env` 파일:

```env
OPENAI_API_KEY=your-api-key-here
DATABASE_URL=sqlite:///./market_analytics.db
```

### Netlify

Netlify 대시보드 → Site settings → Environment variables:

- `OPENAI_API_KEY`: OpenAI API 키
- `DATABASE_URL`: (선택사항) 외부 데이터베이스 URL

---

## 데이터베이스

### 로컬 개발

- 기본: SQLite (`market_analytics.db`)
- 파일이 자동으로 생성됩니다

### Netlify 배포

- SQLite는 Netlify Functions와 호환되지 않음
- 외부 데이터베이스 권장:
  - Supabase (PostgreSQL)
  - MongoDB Atlas
  - Railway (PostgreSQL)

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

### Netlify Functions 로컬 테스트 오류

```bash
# Netlify CLI 재설치
npm install -g netlify-cli

# 로그인 확인
netlify login

# 다시 시도
npm run netlify:dev
```

---

## 프로젝트 구조

```
application-market-analytics/
├── app/                    # FastAPI 애플리케이션
│   ├── main.py            # 메인 앱
│   ├── routers/           # API 라우터
│   ├── services/          # 비즈니스 로직
│   └── models.py          # 데이터베이스 모델
├── netlify/               # Netlify Functions
│   └── functions/
│       └── server.py      # 서버리스 함수 엔트리 포인트
├── templates/             # HTML 템플릿
├── static/                # 정적 파일 (CSS, JS)
├── netlify.toml           # Netlify 설정
├── requirements.txt       # Python 의존성
└── package.json           # npm 스크립트
```

