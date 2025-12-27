# Netlify 배포 가이드

## 📋 배포 전 확인 사항

### 1. 프로젝트 구조
- ✅ `netlify.toml` - Netlify 설정 파일
- ✅ `package.json` - npm 스크립트 설정
- ✅ `netlify/functions/server.py` - 서버리스 함수 엔트리 포인트
- ✅ `requirements.txt` - Python 의존성 (mangum 포함)
- ✅ `runtime.txt` - Python 버전 지정

### 2. 필요한 패키지
- `mangum` - FastAPI를 서버리스 함수로 변환

## 🚀 배포 방법

### 방법 1: Netlify CLI 사용 (권장)

#### 1. Netlify CLI 설치
```bash
npm install -g netlify-cli
```

#### 2. 로그인
```bash
netlify login
```

#### 3. 배포
```bash
# 초기 설정 (처음 한 번만)
netlify init

# 배포
netlify deploy --prod
```

### 방법 2: Git 연동 (권장)

#### 1. GitHub에 프로젝트 푸시
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

#### 2. Netlify 대시보드에서 설정
1. https://app.netlify.com 접속
2. "Add new site" → "Import an existing project"
3. GitHub 선택 후 저장소 연결
4. 빌드 설정:
   - Build command: `pip install -r requirements.txt`
   - Publish directory: `.` (또는 빈 값)
   - Functions directory: `netlify/functions`
5. 환경 변수 설정:
   - `OPENAI_API_KEY`: OpenAI API 키 (선택사항)

#### 3. 배포
- Git에 푸시하면 자동으로 배포됩니다

## 🔧 환경 변수 설정

Netlify 대시보드에서 환경 변수 설정:

1. Site settings → Environment variables
2. 다음 변수 추가:
   - `OPENAI_API_KEY`: OpenAI API 키 (AI 리포트 기능 사용 시)

## 📝 중요 사항

### 데이터베이스
- 현재 SQLite를 사용하고 있지만, Netlify Functions는 읽기 전용 파일 시스템을 사용합니다
- **해결 방법**:
  1. **PostgreSQL/MongoDB 같은 외부 데이터베이스 사용** (권장)
  2. 또는 **SQLite 파일을 Netlify Functions의 `/tmp` 디렉토리에 저장** (임시 방안)

### 파일 저장소
- 업로드된 파일은 `/tmp` 디렉토리에 저장되지만, 함수 실행 간에 유지되지 않습니다
- **해결 방법**: S3, Cloudinary 등 외부 스토리지 사용

### 타임아웃
- Netlify Functions는 기본 10초, 최대 26초 타임아웃
- 긴 작업은 비동기로 처리하거나 별도 서비스 사용 권장

## 🔄 데이터베이스 마이그레이션 (권장)

### PostgreSQL 사용 예시

1. **requirements.txt에 추가**:
```
psycopg2-binary==2.9.9
```

2. **database.py 수정**:
```python
import os
from sqlalchemy import create_engine

# 환경 변수에서 데이터베이스 URL 가져오기
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./market_analytics.db"
)

# PostgreSQL URL 형식 변환 (Netlify Functions용)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
```

3. **Netlify 환경 변수에 추가**:
```
DATABASE_URL=postgresql://user:password@host:port/database
```

## 🧪 로컬 테스트

### Netlify Functions 로컬 테스트
```bash
# Netlify CLI로 로컬 개발 서버 실행
netlify dev
```

이렇게 하면:
- 로컬에서 Netlify Functions 환경 시뮬레이션
- API 엔드포인트: http://localhost:8888/.netlify/functions/server

## 📊 배포 후 확인

1. **사이트 URL 확인**: Netlify 대시보드에서 배포된 URL 확인
2. **API 엔드포인트 테스트**: `https://your-site.netlify.app/api/apps/`
3. **기능 테스트**:
   - 대시보드: `https://your-site.netlify.app/`
   - 앱 관리: `https://your-site.netlify.app/apps`
   - 분석: `https://your-site.netlify.app/analysis`
   - AI 리포트: `https://your-site.netlify.app/report`

## ⚠️ 제한 사항

1. **함수 실행 시간**: 최대 26초
2. **파일 시스템**: 읽기 전용 (임시 디렉토리 `/tmp` 사용 가능)
3. **메모리**: 기본 128MB, 최대 3GB
4. **데이터베이스**: SQLite는 권장하지 않음 (PostgreSQL 등 사용)

## 🔍 문제 해결

### 빌드 실패
- Python 버전 확인: `runtime.txt`에 올바른 버전 지정
- 의존성 확인: `requirements.txt`에 모든 패키지 포함

### 함수 실행 오류
- 로그 확인: Netlify 대시보드 → Functions → Logs
- 환경 변수 확인: 올바르게 설정되었는지 확인

### 데이터베이스 오류
- 외부 데이터베이스 사용 권장
- SQLite는 Netlify Functions와 호환되지 않음

## 📚 참고 자료

- [Netlify Functions 문서](https://docs.netlify.com/functions/overview/)
- [Mangum 문서](https://mangum.io/)
- [FastAPI 배포 가이드](https://fastapi.tiangolo.com/deployment/)

