# 🚀 Netlify 배포 단계별 가이드

## ✅ 준비 완료

- [x] Netlify CLI 설치 완료 (v23.13.0)
- [x] 필수 파일 준비 완료
- [x] 서버리스 함수 핸들러 확인 완료

## 배포 진행

### 1단계: Netlify 로그인
```bash
netlify login
```
이 명령어를 실행하면 브라우저가 열리고 Netlify 로그인을 요청합니다.

### 2단계: 프로젝트 초기화
```bash
cd /Users/donghakim/Desktop/application/016-Application-market-analytics
netlify init
```

**초기화 시 선택 옵션:**
1. **"Create & configure a new site"** 선택
2. 팀 선택 (개인 계정 또는 조직)
3. 사이트 이름 입력 (예: `application-market-analytics`) 또는 Enter로 기본값 사용
4. Build command: **Enter** (netlify.toml에서 이미 설정됨)
5. Publish directory: **`.`** (또는 Enter)

### 3단계: 환경 변수 설정 (중요!)

**방법 1: CLI로 설정**
```bash
netlify env:set OPENAI_API_KEY "your-actual-api-key-here"
```

**방법 2: Netlify 대시보드에서 설정**
1. https://app.netlify.com 접속
2. 사이트 선택
3. Site settings → Environment variables
4. "Add a variable" 클릭
5. Key: `OPENAI_API_KEY`, Value: `your-api-key`
6. "Save" 클릭

### 4단계: 배포

**테스트 배포 (미리보기)**
```bash
netlify deploy
```

**프로덕션 배포**
```bash
netlify deploy --prod
```

## 배포 후 확인

배포가 완료되면 Netlify가 제공하는 URL이 표시됩니다:
- 예: `https://your-site-name-12345.netlify.app`

### 테스트할 페이지:
- 메인: `https://your-site.netlify.app/`
- 대시보드: `https://your-site.netlify.app/`
- 앱 관리: `https://your-site.netlify.app/apps`
- 분석: `https://your-site.netlify.app/analysis`
- AI 리포트: `https://your-site.netlify.app/report`
- API: `https://your-site.netlify.app/api/apps/`

## 문제 해결

### 로그 확인
```bash
netlify logs:functions
```

또는 Netlify 대시보드에서:
- Functions → Logs

### 빌드 오류 확인
```bash
netlify logs
```

### 로컬 테스트
```bash
netlify dev
```

## ⚠️ 중요 참고사항

1. **데이터베이스**: SQLite는 Netlify Functions와 호환되지 않습니다
   - 프로덕션에서는 PostgreSQL, MongoDB 등 외부 DB 사용 필요
   
2. **환경 변수**: 반드시 Netlify 대시보드에서 설정해야 합니다

3. **함수 타임아웃**: 최대 26초 (긴 작업은 비동기 처리 필요)


