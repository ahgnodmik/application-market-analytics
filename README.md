# Application Market Analytics

안드로이드 마켓(Play Store) 상위 앱을 분석하여 **구현 난이도가 낮고 시장성이 검증된 앱 타입**을 추출하는 내부용 분석 서비스입니다.

## 기능

- 📱 앱 데이터 입력 및 CSV 업로드
- 🔧 기능 단위 분해 및 관리
- 📊 구현 난이도 자동 계산 (0~2점)
- 💰 시장성 신호 점수 자동 계산 (0~10점)
- 📈 2축 매트릭스 시각화
- 🎯 앱 타입 그룹화 및 추천
- 🤖 **ChatGPT 기반 AI 리포트 생성**
- 🎨 **Notion 스타일의 깔끔한 UI** (Tailwind CSS)
- 📦 **Play Store 데이터 자동 수집** (매주 월요일)

## 설치 및 실행

### 빠른 시작

```bash
# 1. Python 의존성 설치
pip install -r requirements.txt

# 2. Node.js 의존성 설치 및 CSS 빌드
npm install

# 3. 환경 변수 설정 (선택사항)
cp .env.example .env
# .env 파일에 OPENAI_API_KEY 등 설정

# 4. 로컬 개발 서버 실행
npm run dev

# 또는 Python 직접 실행
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### CSS 빌드

Tailwind CSS는 빌드된 파일(`static/style.css`)이 Git에 포함되어 있습니다.
개발 중 스타일을 변경한 경우:

```bash
npm run build:css
```

### Railway 배포

Railway에 배포되어 있습니다. 빌드 시 `npm install`이 실행되며, `postinstall` 스크립트가 자동으로 CSS를 빌드합니다.

**중요**: Railway에서 PostgreSQL 데이터베이스를 추가하고 `DATABASE_URL` 환경 변수가 자동으로 설정되어야 합니다.

### 브라우저 접속

서버 실행 후 브라우저에서 접속:
- **메인 대시보드**: http://localhost:8000
- **API 문서 (Swagger)**: http://localhost:8000/docs
- **헬스 체크**: http://localhost:8000/health
- **앱 관리 페이지**: http://localhost:8000/apps
- **분석 페이지**: http://localhost:8000/analysis

## 환경 변수

### 필수
- `DATABASE_URL`: PostgreSQL 연결 문자열 (Railway에서 자동 설정)
- `PORT`: 서버 포트 (Railway에서 자동 설정)

### 선택
- `OPENAI_API_KEY`: OpenAI API 키 (GPT 분석 기능용)
- `APP_ENV`: `prod` / `dev` (기본값: `dev`)
- `LOG_LEVEL`: `INFO` / `DEBUG` (기본값: `INFO`)

## 사용 방법

1. 대시보드에서 앱 데이터 입력
2. 각 앱의 기능을 분해하여 입력
3. 자동으로 점수가 계산됨
4. 필터 조건 설정하여 후보 앱 타입 확인

## 필터링 조건

- 시장성 점수 ≥ 6
- 구현 난이도 ≤ 1.0
- 핵심 기능 수 ≤ 5
