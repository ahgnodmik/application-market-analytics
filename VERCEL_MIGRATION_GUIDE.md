# 🚀 Vercel로 마이그레이션 가이드

## 왜 Vercel인가?

- ✅ **Python Functions 완전 지원** - FastAPI 그대로 사용 가능
- ✅ **자동 배포** - GitHub 푸시 시 자동 배포
- ✅ **무료 티어** - 충분한 사용량 제공
- ✅ **빠른 설정** - 몇 분 만에 배포 완료

## 현재 문제점

- ❌ Netlify는 Python Functions를 제한적으로 지원
- ❌ 실제 기능들 (순위 매기기, 분석, 리포트)이 작동하지 않음
- ❌ JavaScript 함수만 작동하여 기본 페이지만 표시

## 마이그레이션 단계

### 1. Vercel 계정 생성

1. https://vercel.com 접속
2. GitHub 계정으로 로그인 (또는 이메일로 가입)

### 2. 프로젝트 연결

1. Vercel 대시보드에서 **"Add New..."** → **"Project"** 클릭
2. GitHub 저장소 선택: `ahgnodmik/application-market-analytics`
3. **"Import"** 클릭

### 3. 빌드 설정

Vercel이 자동으로 감지하지만, 확인:
- **Framework Preset**: Other
- **Root Directory**: `./` (기본값)
- **Build Command**: (비워두기 - 자동 감지)
- **Output Directory**: (비워두기)
- **Install Command**: `pip install -r requirements.txt`

### 4. 환경 변수 설정

**Environment Variables** 섹션에서:
- `OPENAI_API_KEY`: OpenAI API 키 (기존과 동일)

### 5. 배포

**"Deploy"** 버튼 클릭 → 자동 배포 시작

## 파일 변경사항

### 추가된 파일

1. **`vercel.json`**: Vercel 설정 파일
   - Python Functions 설정
   - 라우팅 규칙

2. **`api/index.py`**: Vercel Functions 엔트리 포인트
   - FastAPI 앱을 Mangum으로 래핑
   - Vercel Functions 형식으로 변환

## 대안: Railway 사용 (더 간단할 수 있음)

Railway는 더 간단할 수 있습니다:

### Railway 배포

1. https://railway.app 접속
2. **"New Project"** → **"Deploy from GitHub repo"**
3. 저장소 선택
4. **"Deploy"** 클릭
5. 환경 변수 추가: `OPENAI_API_KEY`

**장점:**
- 더 간단한 설정
- 데이터베이스 자동 제공 (PostgreSQL)
- 파일 시스템 쓰기 가능

## 현재 상태 vs Vercel 마이그레이션 후

### 현재 (Netlify)
- ✅ 웹사이트 표시
- ❌ Python FastAPI 앱 작동 안함
- ❌ 순위 매기기 기능 없음
- ❌ 분석 기능 없음
- ❌ 리포트 생성 없음

### Vercel 마이그레이션 후
- ✅ 웹사이트 표시
- ✅ Python FastAPI 앱 작동
- ✅ 순위 매기기 기능 작동 (`/api/analysis/`)
- ✅ 분석 기능 작동 (`/analysis`)
- ✅ 리포트 생성 작동 (`/report`)
- ✅ 앱 관리 기능 작동 (`/apps`)

## 테스트

마이그레이션 후 다음 URL로 테스트:

- 메인: `https://your-project.vercel.app/`
- 앱 목록: `https://your-project.vercel.app/apps`
- 분석: `https://your-project.vercel.app/analysis`
- API: `https://your-project.vercel.app/api/apps/`

## 롤백 (필요 시)

Netlify는 그대로 유지되므로:
- Netlify URL로 계속 접근 가능
- Vercel이 작동하지 않으면 Netlify로 다시 돌아가기 가능

## 다음 단계

1. Vercel 계정 생성
2. GitHub 저장소 연결
3. 환경 변수 설정
4. 배포
5. 테스트

**예상 소요 시간: 10-15분**
