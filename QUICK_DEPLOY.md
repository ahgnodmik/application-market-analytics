# 🚀 Netlify 빠른 배포 가이드

## 방법 1: Netlify CLI 사용 (가장 빠름)

### 1단계: Netlify CLI 설치
```bash
npm install -g netlify-cli
```

### 2단계: 로그인
```bash
netlify login
```

### 3단계: 프로젝트 디렉토리에서 배포
```bash
cd /Users/donghakim/Desktop/application/016-Application-market-analytics

# 초기 설정 (처음 한 번만)
netlify init

# 배포 옵션 선택:
# - Create & configure a new site
# - Site name: (원하는 이름 입력)
# - Build command: (빈 값으로 Enter, netlify.toml에서 설정됨)
# - Publish directory: . (또는 빈 값)
```

### 4단계: 환경 변수 설정
```bash
netlify env:set OPENAI_API_KEY "your-api-key-here"
```

### 5단계: 배포
```bash
# 미리보기 배포
netlify deploy

# 프로덕션 배포
netlify deploy --prod
```

## 방법 2: Git 연동 (자동 배포)

### 1단계: GitHub에 푸시
```bash
git init
git add .
git commit -m "Initial commit for Netlify deployment"
git remote add origin <your-github-repo-url>
git push -u origin main
```

### 2단계: Netlify 대시보드에서 설정

1. **https://app.netlify.com** 접속
2. **"Add new site"** → **"Import an existing project"**
3. GitHub 선택 후 저장소 연결
4. **빌드 설정** (자동으로 `netlify.toml`을 읽습니다):
   - Build command: `pip install -r requirements.txt`
   - Publish directory: `.`
   - Functions directory: `netlify/functions`
5. **"Deploy site"** 클릭

### 3단계: 환경 변수 설정

배포 후:
1. Site settings → **Environment variables**
2. **"Add a variable"** 클릭
3. 다음 변수 추가:
   - Key: `OPENAI_API_KEY`
   - Value: `your-api-key-here`
4. **"Save"** 클릭
5. **"Trigger deploy"** → **"Clear cache and deploy site"** 클릭

## 🔍 배포 확인

배포가 완료되면 Netlify가 제공하는 URL로 접속:
- 예: `https://your-site-name.netlify.app`

### 테스트할 엔드포인트:
- 메인: `https://your-site.netlify.app/`
- 대시보드: `https://your-site.netlify.app/`
- 앱 관리: `https://your-site.netlify.app/apps`
- 분석: `https://your-site.netlify.app/analysis`
- AI 리포트: `https://your-site.netlify.app/report`
- API: `https://your-site.netlify.app/api/apps/`

## ⚠️ 중요 사항

### 데이터베이스
- **현재 SQLite 사용 중**: Netlify Functions는 읽기 전용 파일 시스템을 사용하므로 SQLite가 제대로 작동하지 않을 수 있습니다.
- **권장 해결책**: PostgreSQL, MongoDB 등 외부 데이터베이스 사용
  - [Supabase](https://supabase.com) (무료 PostgreSQL)
  - [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) (무료 MongoDB)
  - [Railway](https://railway.app) (PostgreSQL 호스팅)

### 환경 변수
- Netlify 대시보드에서 반드시 설정해야 합니다
- `.env` 파일은 Git에 커밋하지 마세요 (`.gitignore`에 포함됨)

### 로그 확인
- Netlify 대시보드 → Functions → Logs에서 오류 확인
- Site settings → Build & deploy → Deploy log에서 빌드 오류 확인

## 🔧 문제 해결

### 빌드 실패
```bash
# 로컬에서 테스트
netlify build
```

### 함수 실행 오류
- Functions 로그 확인: Netlify 대시보드 → Functions → Logs
- 환경 변수가 올바르게 설정되었는지 확인

### 데이터베이스 오류
- 외부 데이터베이스 사용 (Supabase, MongoDB Atlas 등)
- `DATABASE_URL` 환경 변수 설정

## 📚 상세 가이드

더 자세한 내용은 `NETLIFY_DEPLOY.md` 파일을 참고하세요.

