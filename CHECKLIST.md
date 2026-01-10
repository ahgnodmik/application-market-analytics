# ✅ 웹페이지 문제 해결 체크리스트

## 발견된 문제점

### 1. ❌ 존재하지 않는 파일 참조 (수정 완료)
- `base.html`에서 `/static/main.js` 참조
- 실제로는 `apps.js`와 `analysis.js`만 존재
- ✅ **수정 완료**: `main.js` 참조 제거

### 2. ⚠️ 정적 파일 및 템플릿 경로 (개선 완료)
- Netlify Functions 환경에서 경로 찾기 개선
- 디버깅 로그 추가
- ✅ **개선 완료**: 경로 해결 로직 개선, 로깅 추가

### 3. ⚠️ 디버깅 정보 부족 (개선 완료)
- Functions 실행 시 경로 정보 없음
- ✅ **개선 완료**: 디버깅 로그 추가

## 수정 완료 사항

### ✅ base.html
- 존재하지 않는 `main.js` 참조 제거

### ✅ app/main.py
- 경로 해결 로직 개선
- 디버깅 로그 추가
- Fallback 경로 추가
- Health check에 경로 정보 추가

### ✅ netlify/functions/server.py
- 디버깅 로그 추가
- 경로 정보 출력

## 확인 방법

### 1. Functions 로그 확인
Netlify 대시보드 → Functions → server → Logs에서 다음 메시지 확인:
```
[Netlify Functions] Server.py location: ...
[Netlify Functions] Current dir: ...
[Netlify Functions] Project root: ...
[Netlify Functions] Static exists: True/False
[Netlify Functions] Templates exists: True/False
```

### 2. Health Check 테스트
```
https://app-market-analytics.netlify.app/health
```

응답 예시:
```json
{
  "status": "ok",
  "static_dir_exists": true,
  "templates_dir_exists": true,
  "static_dir": "/var/task/static",
  "templates_dir": "/var/task/templates",
  "project_root": "/var/task"
}
```

### 3. 직접 접속 테스트
- 메인 페이지: `https://app-market-analytics.netlify.app/`
- 앱 관리: `https://app-market-analytics.netlify.app/apps`
- 분석: `https://app-market-analytics.netlify.app/analysis`
- AI 리포트: `https://app-market-analytics.netlify.app/report`

## 다음 단계

1. **배포 완료 확인**
   - 변경사항이 GitHub에 푸시되었습니다
   - Netlify가 자동으로 다시 배포합니다

2. **Functions 로그 확인**
   - Netlify 대시보드 → Functions → server → Logs
   - 디버깅 메시지 확인
   - 오류 메시지 확인

3. **Health Check 테스트**
   - `/health` 엔드포인트로 경로 정보 확인

4. **문제가 지속되는 경우**
   - Functions 로그의 전체 오류 메시지 공유
   - Health Check 응답 공유
   - 브라우저 개발자 도구의 네트워크 탭 확인

## 주요 포인트

### 정적 파일 서빙
- Netlify Functions는 모든 요청을 함수로 라우팅합니다
- 정적 파일도 Functions를 통해 서빙되어야 합니다
- `app.mount("/static", ...)`로 FastAPI가 정적 파일을 서빙합니다

### 템플릿 파일
- 템플릿 파일은 Functions 패키지에 포함되어야 합니다
- Git에 커밋되어 있어야 합니다
- `.gitignore`에서 제외되지 않아야 합니다

### 데이터베이스
- SQLite는 `/tmp` 디렉토리 사용 (임시)
- 프로덕션에서는 외부 DB 권장 (Supabase, MongoDB Atlas 등)
