# 🔧 Railway 502 Bad Gateway 에러 해결

## 문제

Railway에서 `502 Bad Gateway` 에러 발생

## 원인 가능성

1. 앱이 시작되지 않음
2. 앱 초기화 중 크래시
3. 포트 설정 문제
4. 경로 해결 실패

## 적용한 수정 사항

### 1. 에러 핸들링 개선

- 데이터베이스 초기화 실패해도 앱 계속 시작
- 라우터 등록 실패해도 로그만 출력
- 상세한 로그 메시지 추가

### 2. 경로 해결 개선

- Railway 환경에서 `os.getcwd()` 확인
- 프로젝트 루트를 더 정확하게 찾음
- 템플릿/정적 파일 경로 fallback 강화

### 3. 시작 명령어 개선

- `--log-level info` 추가로 상세 로그
- 포트 기본값 설정 (`${PORT:-8000}`)

## 확인 방법

### Railway 로그 확인

1. Railway 대시보드 → 프로젝트 선택
2. **"Deployments"** 탭 → 최신 배포 클릭
3. **"View Logs"** 클릭
4. 다음 메시지 확인:
   - `[APP INIT] ✅ Database tables created successfully`
   - `[APP INIT] ✅ All routers registered successfully`
   - `Application startup complete`
   - `Uvicorn running on http://0.0.0.0:PORT`

### 에러가 있다면

로그에서 다음 확인:
- `[APP INIT] ⚠️ Warning:` 메시지
- Python traceback
- Import 에러

## 추가 디버깅

### 로컬에서 테스트

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 환경 변수 확인

Railway 대시보드에서:
- `OPENAI_API_KEY` 설정되어 있는지 확인
- `PORT` 환경 변수가 자동으로 설정되는지 확인

## 다음 단계

1. 변경사항 푸시 완료 → Railway 자동 재배포
2. 배포 완료 후 로그 확인
3. 502 에러가 사라졌는지 확인
4. 정상 작동 확인

## 예상 결과

배포 성공 시:
- ✅ 로그에 `Application startup complete` 메시지
- ✅ 502 에러 없음
- ✅ 웹사이트 정상 접속
- ✅ 모든 기능 작동
