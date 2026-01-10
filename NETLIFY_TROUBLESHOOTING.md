# 🔧 Netlify 서비스 표시 문제 해결 가이드

## 문제 진단

Netlify에서 서비스가 정상 표시되지 않는 경우 다음을 확인하세요.

## 주요 수정 사항

### 1. 템플릿 로딩 개선 ✅

**문제**: Netlify Functions 환경에서 템플릿 경로를 찾지 못함

**해결**:
- 여러 경로를 시도하는 fallback 로직 추가
- Netlify Functions 기본 경로 (`/var/task/`) 추가
- 에러 핸들링 개선

### 2. 에러 핸들링 추가 ✅

**문제**: 템플릿 로드 실패 시 앱이 완전히 실패함

**해결**:
- 각 라우트에 try-except 추가
- 템플릿이 없어도 에러 메시지 표시
- Health check 엔드포인트 개선

## 진단 방법

### 1. Health Check 확인

```bash
curl https://app-market-analytics.netlify.app/health
```

응답에서 확인할 사항:
- `status`: "ok" 또는 "error"
- `templates_loaded`: true/false
- `paths`: 각 경로의 존재 여부
- `template_dirs_checked`: 시도한 템플릿 경로들

### 2. Functions 로그 확인

Netlify 대시보드 → Functions → server → Logs

확인할 메시지:
```
[Netlify Functions] Server.py location: ...
[Netlify Functions] Project root: ...
Templates loaded from: ...
```

### 3. 브라우저 개발자 도구

- Network 탭: 요청이 실패하는지 확인
- Console 탭: JavaScript 오류 확인
- Response: 실제 HTML 응답 확인

## 가능한 원인 및 해결

### 원인 1: 템플릿 파일이 Functions 패키지에 포함되지 않음

**확인**:
```bash
# 로컬에서 확인
ls -la templates/
ls -la static/
```

**해결**:
- `templates/`와 `static/` 디렉토리가 Git에 포함되어 있는지 확인
- `.gitignore`에서 제외되지 않았는지 확인

### 원인 2: 경로 문제

**확인**: Health check 응답에서 `template_dirs_checked` 확인

**해결**: 
- 여러 fallback 경로 시도 (이미 구현됨)
- 필요시 `/var/task/` 경로 확인

### 원인 3: 데이터베이스 초기화 실패

**확인**: Functions 로그에서 다음 메시지 확인
```
Warning: Database initialization failed: ...
```

**해결**:
- 예외 처리로 앱은 시작되지만 데이터 저장 불가
- 프로덕션에서는 외부 DB 사용 권장

### 원인 4: 정적 파일 경로 문제

**확인**: 브라우저 개발자 도구 → Network → `/static/` 요청 확인

**해결**:
- `app.mount("/static", ...)` 설정 확인
- 정적 파일도 Functions를 통해 서빙됨 (정상)

## 테스트 단계

### Step 1: 기본 접속 테스트
```
https://app-market-analytics.netlify.app/health
```
- 200 응답 확인
- JSON 응답 구조 확인

### Step 2: 메인 페이지 테스트
```
https://app-market-analytics.netlify.app/
```
- HTML 응답 확인
- 템플릿이 로드되었는지 확인

### Step 3: 정적 파일 테스트
```
https://app-market-analytics.netlify.app/static/apps.js
```
- JavaScript 파일 응답 확인
- 또는 404 응답 (Functions를 통해 서빙되므로)

### Step 4: API 엔드포인트 테스트
```
https://app-market-analytics.netlify.app/api/apps/
```
- JSON 응답 확인
- 빈 배열 `[]` 응답도 정상 (데이터가 없는 경우)

## 추가 디버깅

### Functions 로그에서 확인할 내용

1. **템플릿 로드 메시지**:
   ```
   Templates loaded from: /var/task/templates
   ```

2. **경로 확인 메시지**:
   ```
   Current file: ...
   Current dir: ...
   Project root: ...
   Static dir exists: True/False
   Templates dir exists: True/False
   ```

3. **에러 메시지**:
   ```
   Error rendering dashboard: ...
   CRITICAL: Failed to load templates: ...
   ```

### 로컬에서 테스트

```bash
# Netlify Functions 로컬 시뮬레이션
npm run netlify:dev
```

또는

```bash
netlify dev
```

## 다음 단계

1. ✅ 템플릿 로딩 개선 (완료)
2. ✅ 에러 핸들링 추가 (완료)
3. ⏳ Health check로 상태 확인
4. ⏳ Functions 로그 확인
5. ⏳ 필요시 추가 수정

## 임시 해결책

만약 여전히 작동하지 않는다면:

### 임시 해결책 1: 간단한 HTML 응답

템플릿 대신 직접 HTML 문자열 반환:

```python
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return HTMLResponse(content="<h1>서비스 준비 중</h1>")
```

### 임시 해결책 2: 정적 파일로 HTML 제공

Netlify의 정적 파일 호스팅 사용 (Functions 없이)

## 연락처

문제가 지속되면 다음 정보와 함께 문의:
1. Health check 응답 전체
2. Functions 로그 (최근 50줄)
3. 브라우저 개발자 도구 스크린샷
