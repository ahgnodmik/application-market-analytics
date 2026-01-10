# 🚂 Railway 배포 가이드 (권장)

## 왜 Railway인가?

Vercel에서 계속 빌드 실패가 발생하므로, **Railway가 더 간단하고 안정적**입니다:

✅ **간단한 설정** - `Procfile` 하나면 끝
✅ **Python 완벽 지원** - FastAPI 그대로 실행
✅ **데이터베이스 자동 제공** - PostgreSQL 무료
✅ **파일 시스템 쓰기 가능** - SQLite도 사용 가능
✅ **환경 변수 쉬운 설정**

## 배포 단계 (5-10분)

### 1. Railway 계정 생성

1. https://railway.app 접속
2. "Login" 클릭 → GitHub 계정으로 로그인

### 2. 새 프로젝트 생성

1. Railway 대시보드에서 **"New Project"** 클릭
2. **"Deploy from GitHub repo"** 선택
3. 저장소 선택: `ahgnodmik/application-market-analytics`
4. 자동으로 배포 시작

### 3. 환경 변수 설정

Railway 대시보드에서:
1. 프로젝트 선택
2. **"Variables"** 탭 클릭
3. **"New Variable"** 클릭
4. 추가:
   - `OPENAI_API_KEY`: `sk-proj-...` (기존 키)

### 4. 배포 확인

배포가 완료되면:
- Railway가 자동으로 URL 제공: `https://your-project.up.railway.app`
- 브라우저에서 접속하여 테스트

## 필요한 파일 (이미 준비됨)

✅ `Procfile` - Railway가 Python 앱을 실행하는 방법 지정
✅ `requirements.txt` - Python 의존성
✅ `.python-version` - Python 버전 (선택사항)

## 추가 설정 (선택)

### PostgreSQL 사용 (권장)

1. Railway 대시보드에서 **"New"** → **"Database"** → **"Add PostgreSQL"**
2. 자동으로 `DATABASE_URL` 환경 변수 생성됨
3. `app/database.py`에서 자동으로 PostgreSQL 사용

### 도메인 설정 (선택)

1. Railway 프로젝트 → **"Settings"** → **"Generate Domain"**
2. 또는 커스텀 도메인 추가

## 현재 vs Railway

| 기능 | 현재 (Vercel) | Railway |
|------|--------------|---------|
| Python 지원 | ⚠️ 제한적 | ✅ 완벽 |
| FastAPI | ❌ 작동 안함 | ✅ 완벽 |
| 설정 복잡도 | ⚠️ 복잡 | ✅ 매우 간단 |
| 데이터베이스 | ❌ 추가 설정 필요 | ✅ 자동 제공 |
| 배포 속도 | ⚠️ 느림 (실패) | ✅ 빠름 |

## 예상 시간

- 계정 생성: 1분
- 프로젝트 연결: 1분
- 환경 변수 설정: 1분
- 배포 대기: 2-3분
- **총 5-10분**

## 다음 단계

1. Railway 접속 및 로그인
2. GitHub 저장소 연결
3. 환경 변수 설정
4. 배포 완료 대기
5. 테스트!
