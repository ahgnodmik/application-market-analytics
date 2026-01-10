# 🔍 웹페이지 작동 불가 문제 진단 및 수정

## 문제점

웹에서 아무것도 나타나지 않습니다.

## 주요 문제점

### 1. 존재하지 않는 파일 참조 ❌
- `base.html`에서 `/static/main.js` 참조하지만 실제로는 파일이 없음
- `apps.js`와 `analysis.js`만 존재

### 2. 정적 파일 및 템플릿 경로 문제
- Netlify Functions 환경에서 프로젝트 루트 경로를 찾지 못할 수 있음
- 디버깅 정보가 부족함

### 3. 디버깅 부족
- Functions 실행 시 경로 정보가 없어 문제 진단이 어려움

## 수정 사항

### 1. base.html 수정
- 존재하지 않는 `main.js` 참조 제거

### 2. app/main.py 경로 해결 개선
- 여러 경로 시나리오 고려
- 디버깅 로그 추가
- Fallback 경로 추가

### 3. netlify/functions/server.py 디버깅 추가
- 경로 정보 로깅
- 정적 파일 및 템플릿 디렉토리 존재 여부 확인

### 4. Health Check 개선
- 경로 정보 포함하여 상태 확인 가능

## 확인 방법

### 1. Netlify Functions 로그 확인
Netlify 대시보드 → Functions → server → Logs:
```
[Netlify Functions] Server.py location: ...
[Netlify Functions] Current dir: ...
[Netlify Functions] Project root: ...
[Netlify Functions] Static exists: True/False
[Netlify Functions] Templates exists: True/False
```

### 2. Health Check 엔드포인트 테스트
```
https://app-market-analytics.netlify.app/health
```

응답 예시:
```json
{
  "status": "ok",
  "static_dir_exists": true,
  "templates_dir_exists": true,
  "project_root": "/var/task/..."
}
```

### 3. 직접 접속 테스트
- 메인 페이지: `https://app-market-analytics.netlify.app/`
- 헬스 체크: `https://app-market-analytics.netlify.app/health`
- 정적 파일: `https://app-market-analytics.netlify.app/static/apps.js`

## 가능한 추가 문제

### Netlify Functions에서 정적 파일 서빙 제한
Netlify Functions는 모든 요청을 함수로 라우팅합니다. 정적 파일도 Functions를 통해 서빙되어야 합니다.

**확인 사항:**
1. Functions 로그에서 정적 파일 요청이 처리되는지 확인
2. 404 오류가 발생하는지 확인
3. 템플릿 렌더링 오류가 있는지 확인

### 템플릿 파일이 Functions에 포함되지 않음
Netlify Functions는 함수 디렉토리와 의존성만 포함합니다. 프로젝트의 다른 파일들도 포함되어야 합니다.

**해결책:**
- `templates/`와 `static/` 디렉토리가 Git에 포함되어 있는지 확인
- `.gitignore`에서 제외되지 않았는지 확인

## 다음 단계

1. **배포 확인**
   - 변경사항이 푸시되었습니다
   - Netlify가 자동으로 다시 배포합니다

2. **Functions 로그 확인**
   - Netlify 대시보드 → Functions → server → Logs
   - 디버깅 메시지 확인
   - 오류 메시지 확인

3. **Health Check 테스트**
   - `/health` 엔드포인트로 경로 정보 확인

4. **문제가 지속되는 경우**
   - Functions 로그의 전체 오류 메시지 확인
   - 정적 파일 요청이 Functions로 라우팅되는지 확인
   - 템플릿 파일이 Functions 패키지에 포함되는지 확인
