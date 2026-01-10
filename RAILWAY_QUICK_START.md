# 🚀 Railway 빠른 시작 가이드

## 1단계: Railway 계정 생성 (1분)

1. https://railway.app 접속
2. **"Login"** 클릭
3. **"Login with GitHub"** 선택
4. GitHub 계정으로 로그인

## 2단계: 프로젝트 배포 (2분)

1. Railway 대시보드에서 **"New Project"** 클릭
2. **"Deploy from GitHub repo"** 선택
3. 저장소 검색: `application-market-analytics`
4. 저장소 선택: `ahgnodmik/application-market-analytics`
5. **"Deploy Now"** 클릭

→ Railway가 자동으로 배포를 시작합니다!

## 3단계: 환경 변수 설정 (1분)

배포가 시작되면:

1. 프로젝트 대시보드에서 **"Variables"** 탭 클릭
2. **"New Variable"** 클릭
3. 다음 추가:
   - **Name**: `OPENAI_API_KEY`
   - **Value**: `.env.local` 파일에 있는 API 키 값 입력
4. **"Add"** 클릭

> 💡 **참고**: API 키는 `.env.local` 파일에 있습니다. 보안을 위해 직접 복사해서 붙여넣으세요.

## 4단계: 배포 완료 대기 (2-3분)

Railway 대시보드에서:
- 배포 상태 확인 (진행 중 → 완료)
- 로그 확인 (에러가 없으면 OK)

## 5단계: URL 확인 및 테스트

배포 완료 후:

1. 프로젝트 대시보드에서 **"Settings"** 탭 클릭
2. **"Generate Domain"** 클릭 (또는 자동 생성됨)
3. URL 확인: `https://your-project.up.railway.app`

### 테스트 URL

- 메인 페이지: `https://your-project.up.railway.app/`
- 앱 목록: `https://your-project.up.railway.app/apps`
- 분석 (순위 매기기): `https://your-project.up.railway.app/analysis`
- 리포트: `https://your-project.up.railway.app/report`
- API 문서: `https://your-project.up.railway.app/docs`

## ✅ 완료!

이제 모든 기능이 작동합니다:
- ✅ 구글 앱스토어 순위 매기기
- ✅ 앱 분석
- ✅ AI 리포트 생성
- ✅ 앱 관리

## 문제 해결

### 배포 실패 시

1. **"Deployments"** 탭에서 로그 확인
2. 에러 메시지 확인
3. 주로 환경 변수 누락 문제

### 데이터베이스 사용 (선택)

PostgreSQL 사용하려면:
1. 프로젝트에서 **"New"** → **"Database"** → **"Add PostgreSQL"**
2. 자동으로 `DATABASE_URL` 환경 변수 생성됨
3. `app/database.py`가 자동으로 PostgreSQL 사용

## 예상 소요 시간

- 계정 생성: 1분
- 프로젝트 연결: 1분
- 환경 변수 설정: 1분
- 배포 대기: 2-3분
- **총 5-7분**
