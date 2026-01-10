# 🔍 Netlify 웹사이트 표시 문제 최종 진단 가이드

## 문제 현황

여전히 웹사이트가 표시되지 않는 경우, 다음 단계를 따라 확인하세요.

## 1단계: Health Check 확인

### URL 접속
```
https://app-market-analytics.netlify.app/health
```

### 예상 응답
```json
{
  "status": "ok" 또는 "error",
  "templates_loaded": true/false,
  "static_mounted": true/false,
  "paths": {...},
  "template_dirs_checked": [...],
  "files": {...}
}
```

### 확인 사항
- `status`가 "ok"인지 확인
- `templates_loaded`가 `true`인지 확인
- `files.templates`에 파일 목록이 있는지 확인
- `files.cwd_contents`에 프로젝트 구조가 있는지 확인

## 2단계: Functions 로그 확인

Netlify 대시보드 → Functions → server → Logs

### 확인할 로그 메시지

#### 정상 작동 시:
```
[Netlify Functions] Server.py location: ...
[Netlify Functions] Project root: ...
[APP INIT] Templates loaded from: ...
```

#### 문제 발생 시:
```
[APP INIT] CRITICAL: Failed to load templates: ...
[ERROR] Dashboard render error: ...
```

## 3단계: 테스트 엔드포인트 확인

### 간단한 테스트
```
https://app-market-analytics.netlify.app/test
```

예상 응답:
```json
{
  "message": "서버가 정상적으로 작동 중입니다",
  "timestamp": "2024-01-10"
}
```

이 엔드포인트가 작동한다면:
- ✅ FastAPI 앱은 정상 작동
- ✅ Mangum handler 정상 작동
- ⚠️ 문제는 템플릿/정적 파일 로딩

## 4단계: 메인 페이지 확인

### URL 접속
```
https://app-market-analytics.netlify.app/
```

### 예상 결과

#### 케이스 1: 템플릿 로드 성공
- 정상적인 대시보드 페이지 표시

#### 케이스 2: 템플릿 로드 실패
- 간단한 대시보드 표시 ("서비스 준비 중" 메시지)
- Health Check 링크 제공

#### 케이스 3: 완전 실패
- 빈 페이지 또는 500 에러
- 브라우저 개발자 도구에서 에러 확인

## 5단계: 브라우저 개발자 도구 확인

### Network 탭
1. 페이지 새로고침 (F5)
2. Network 탭에서 요청 확인:
   - `/` 요청 상태 코드 (200, 500, 등)
   - `/static/*` 요청 상태 코드
   - `/health` 요청 상태 코드

### Console 탭
- JavaScript 오류 확인
- 네트워크 오류 확인

### Response 탭
- 실제 HTML 응답 내용 확인
- 에러 메시지 확인

## 주요 수정 사항

### 1. Fallback 대시보드 추가 ✅
- 템플릿을 찾지 못해도 간단한 HTML 페이지 표시
- 사용자가 최소한 Health Check에 접근 가능

### 2. 상세한 Health Check ✅
- 모든 경로 상태 확인
- 파일 목록 확인
- 현재 디렉토리 구조 확인

### 3. 개선된 에러 처리 ✅
- 각 라우트에 try-except 추가
- 상세한 에러 메시지와 traceback

### 4. 디버깅 로그 강화 ✅
- 모든 단계에서 상세 로그 출력
- Functions 로그에서 문제 추적 가능

## 가능한 문제 및 해결책

### 문제 1: 템플릿 파일이 Functions 패키지에 포함되지 않음

**증상**: 
- `templates_loaded: false`
- `files.templates: "Directory does not exist"`

**원인**: 
Netlify Functions는 `netlify/functions/` 디렉토리만 포함하므로, 프로젝트 루트의 `templates/` 디렉토리가 포함되지 않을 수 있습니다.

**해결책**:
1. `templates/` 디렉토리를 `netlify/functions/`로 복사
2. 또는 템플릿을 코드에 임베드

### 문제 2: 경로 문제

**증상**:
- `LAMBDA_TASK_ROOT`가 설정되지 않음
- 모든 경로에서 `exists: false`

**해결책**:
- Health Check에서 실제 경로 확인
- `cwd_contents`에서 실제 파일 구조 확인

### 문제 3: Mangum Handler 문제

**증상**:
- `/test` 엔드포인트도 실패
- Functions 로그에 import 오류

**해결책**:
- `netlify/functions/server.py` 확인
- 의존성 설치 확인

## 다음 조치 사항

1. **Health Check 결과 공유**
   - Health Check 응답 전체를 복사하여 공유
   - 문제 진단에 필수적

2. **Functions 로그 공유**
   - 최근 Functions 로그 50줄 공유
   - 특히 `[APP INIT]` 및 `[ERROR]` 메시지

3. **브라우저 개발자 도구 스크린샷**
   - Network 탭 스크린샷
   - Console 탭 오류 메시지

## 임시 해결책

만약 템플릿 파일이 Functions 패키지에 포함되지 않는 것이 확실하다면:

### 방법 1: 템플릿을 Functions 디렉토리로 복사
```bash
cp -r templates netlify/functions/
cp -r static netlify/functions/
```

### 방법 2: 템플릿을 코드에 임베드
- HTML을 Python 문자열로 변환
- 템플릿 엔진 없이 직접 반환

## 변경사항 적용 완료

✅ 모든 개선 사항이 GitHub에 푸시되었습니다.
✅ Netlify가 자동으로 다시 배포합니다.

배포 완료 후 위 단계를 따라 확인해주세요!
