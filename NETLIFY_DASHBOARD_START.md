# 🌐 Netlify 대시보드에서 시작하기

## 방법 1: Git 연동 (가장 쉬움) ⭐

### 1단계: GitHub에 코드 푸시

```bash
cd /Users/donghakim/Desktop/application/016-Application-market-analytics

# Git 초기화 (아직 안 했다면)
git init

# 모든 파일 추가
git add .

# 커밋
git commit -m "Initial commit for Netlify deployment"

# GitHub 저장소 생성 후 연결
# GitHub에서 새 저장소를 만들고:
git remote add origin https://github.com/your-username/your-repo-name.git
git branch -M main
git push -u origin main
```

### 2단계: Netlify 대시보드에서 사이트 생성

1. **https://app.netlify.com** 접속
2. 로그인 (GitHub 계정으로 로그인 권장)
3. **"Add new site"** 버튼 클릭
4. **"Import an existing project"** 선택
5. **GitHub** 선택
6. 저장소 선택 (방금 푸시한 저장소)
7. **"Connect"** 클릭

### 3단계: 빌드 설정

Netlify가 자동으로 `netlify.toml` 파일을 읽지만, 확인:

- **Build command**: `pip install -r requirements.txt`
- **Publish directory**: `.` (또는 빈 값)
- **Functions directory**: `netlify/functions`

**"Deploy site"** 버튼 클릭

### 4단계: 환경 변수 설정

배포가 시작되면:

1. **Site settings** → **Environment variables**
2. **"Add a variable"** 클릭
3. 다음 변수 추가:
   - **Key**: `OPENAI_API_KEY`
   - **Value**: `your-actual-api-key-here`
4. **"Save"** 클릭
5. **"Trigger deploy"** → **"Clear cache and deploy site"** 클릭

### 5단계: 배포 완료 확인

- 배포가 완료되면 Netlify가 제공하는 URL 확인
- 예: `https://your-site-name-12345.netlify.app`

---

## 방법 2: Netlify CLI 사용

### 1단계: CLI 로그인

```bash
netlify login
```

브라우저가 열리면 Netlify 로그인

### 2단계: 사이트 초기화

```bash
cd /Users/donghakim/Desktop/application/016-Application-market-analytics
netlify init
```

선택 옵션:
- **"Create & configure a new site"**
- 사이트 이름 입력
- Build command: Enter (자동 설정)
- Publish directory: `.`

### 3단계: 환경 변수 설정

```bash
netlify env:set OPENAI_API_KEY "your-api-key-here"
```

### 4단계: 배포

```bash
# 테스트 배포
netlify deploy

# 프로덕션 배포
netlify deploy --prod
```

---

## 방법 3: 드래그 앤 드롭 (간단하지만 제한적)

⚠️ **주의**: 이 방법은 정적 사이트에만 적합합니다. FastAPI 앱은 서버리스 함수가 필요하므로 **방법 1 또는 2를 권장**합니다.

---

## ✅ 배포 후 확인 사항

### 1. 사이트 접속 테스트
- 메인 페이지: `https://your-site.netlify.app/`
- 대시보드: `https://your-site.netlify.app/`
- 앱 관리: `https://your-site.netlify.app/apps`
- 분석: `https://your-site.netlify.app/analysis`
- AI 리포트: `https://your-site.netlify.app/report`

### 2. 로그 확인
- **Functions 로그**: Site → Functions → Logs
- **빌드 로그**: Site → Deploys → 선택한 배포 → Build log

### 3. 환경 변수 확인
- Site settings → Environment variables
- 모든 변수가 올바르게 설정되었는지 확인

---

## 🔧 문제 해결

### 빌드 실패
1. **Build log 확인**: Deploys → Build log
2. **Python 버전 확인**: `runtime.txt`에 `python-3.9` 설정 확인
3. **의존성 확인**: `requirements.txt`에 모든 패키지 포함 확인

### 함수 실행 오류
1. **Functions 로그 확인**: Functions → Logs
2. **환경 변수 확인**: 올바르게 설정되었는지 확인
3. **타임아웃 확인**: 긴 작업은 비동기 처리 필요

### 데이터베이스 오류
- SQLite는 Netlify Functions와 호환되지 않음
- 외부 데이터베이스 사용 필요 (Supabase, MongoDB Atlas 등)

---

## 📚 다음 단계

### 데이터베이스 마이그레이션 (필요 시)

1. **Supabase 사용** (무료 PostgreSQL):
   - https://supabase.com 가입
   - 새 프로젝트 생성
   - Connection string 복사
   - Netlify 환경 변수에 `DATABASE_URL` 추가

2. **MongoDB Atlas 사용** (무료 MongoDB):
   - https://www.mongodb.com/cloud/atlas 가입
   - 클러스터 생성
   - Connection string 복사
   - Netlify 환경 변수에 `DATABASE_URL` 추가

---

## 💡 추천 방법

**방법 1 (Git 연동)**을 가장 추천합니다:
- ✅ 자동 배포 (Git push 시 자동)
- ✅ 버전 관리
- ✅ 배포 히스토리
- ✅ 롤백 가능
- ✅ 브랜치별 미리보기 배포


