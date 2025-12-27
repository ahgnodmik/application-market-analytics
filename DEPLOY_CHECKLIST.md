# ✅ Netlify 배포 체크리스트

배포 전 확인 사항:

## 필수 파일 확인

- [x] `netlify.toml` - 배포 설정
- [x] `package.json` - npm 설정
- [x] `requirements.txt` - Python 의존성 (mangum 포함)
- [x] `netlify/functions/server.py` - 서버리스 함수
- [x] `runtime.txt` - Python 버전

## 배포 단계

### 1. Netlify CLI 설치 및 로그인
```bash
npm install -g netlify-cli
netlify login
```

### 2. 프로젝트 초기화
```bash
cd /Users/donghakim/Desktop/application/016-Application-market-analytics
netlify init
```

선택 옵션:
- **Create & configure a new site** 선택
- 사이트 이름 입력 (또는 기본값 사용)
- Build command: (Enter로 넘어가기 - netlify.toml에서 설정됨)
- Publish directory: `.` (Enter)

### 3. 환경 변수 설정
```bash
netlify env:set OPENAI_API_KEY "your-api-key-here"
```

또는 Netlify 대시보드에서:
- Site settings → Environment variables → Add variable

### 4. 배포
```bash
# 미리보기 배포 (테스트용)
netlify deploy

# 프로덕션 배포
netlify deploy --prod
```

## 배포 후 확인

1. **사이트 URL 확인**: Netlify가 제공하는 URL
2. **기능 테스트**:
   - `/` - 대시보드
   - `/apps` - 앱 관리
   - `/analysis` - 분석
   - `/report` - AI 리포트
3. **로그 확인**: Netlify 대시보드 → Functions → Logs

## ⚠️ 주의사항

### 데이터베이스
- SQLite는 Netlify Functions와 호환되지 않음
- 프로덕션에서는 외부 데이터베이스 필요 (Supabase, MongoDB Atlas 등)

### 환경 변수
- `.env` 파일은 Git에 커밋하지 마세요
- Netlify 대시보드에서 환경 변수 설정 필요

### 함수 타임아웃
- 기본 10초, 최대 26초
- 긴 작업은 비동기 처리 필요

