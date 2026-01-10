# 🔍 Railway 502 에러 확인 체크리스트

## 현재 상태

✅ **로컬 테스트**: 정상 작동
❌ **Railway 배포**: 502 Bad Gateway

## 확인 사항

### 1. Railway 로그 확인 (가장 중요!)

Railway 대시보드에서:
1. 프로젝트 선택
2. **"Deployments"** 탭 → 최신 배포 클릭
3. **"View Logs"** 또는 **"Logs"** 탭 클릭

확인할 메시지:
- ✅ `[INIT] ✅ All modules imported successfully`
- ✅ `🚀 Application Market Analytics Started Successfully!`
- ✅ `Uvicorn running on http://0.0.0.0:PORT`
- ❌ 에러 메시지나 traceback

### 2. 환경 변수 확인

Railway 대시보드 → **"Variables"** 탭:
- ✅ `OPENAI_API_KEY` 설정되어 있는지 확인
- ✅ `PORT`는 Railway가 자동 설정 (직접 설정 불필요)

### 3. 빌드 로그 확인

**"Deployments"** → 빌드 단계 로그:
- ✅ 의존성 설치 성공
- ✅ Python 버전 확인
- ❌ 빌드 에러 확인

### 4. Procfile 확인

현재 설정:
```
web: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT --log-level debug
```

Railway가 이 명령어를 사용하는지 확인

## 일반적인 문제 및 해결

### 문제 1: 포트 설정

**증상**: 앱이 시작되지만 연결 실패
**해결**: `$PORT` 환경 변수 사용 (Railway가 자동 설정)

### 문제 2: 의존성 문제

**증상**: Import 에러
**해결**: `requirements.txt` 확인, `psycopg2-binary` 추가됨

### 문제 3: 데이터베이스 연결

**증상**: DB 초기화 실패
**해결**: Railway에서 PostgreSQL 추가 (선택사항), SQLite도 작동

### 문제 4: 메모리 부족

**증상**: 앱 시작 중 크래시
**해결**: Railway 요금제 확인, 더 큰 인스턴스 사용

## 다음 단계

1. **Railway 로그 확인** - 가장 중요!
2. 에러 메시지가 있으면 공유해주세요
3. 로그가 없다면 Railway 지원팀에 문의

## 디버깅 명령어

Railway CLI 사용 (선택사항):
```bash
railway logs
railway shell
```

## 예상 결과

성공 시 로그:
```
[INIT] Python version: 3.10.x
[INIT] Working directory: /app
[INIT] PORT environment variable: 12345
[INIT] ✅ All modules imported successfully
[APP INIT] ✅ Database tables created successfully
[APP INIT] ✅ All routers registered successfully
🚀 Application Market Analytics Started Successfully!
INFO:     Uvicorn running on http://0.0.0.0:12345
INFO:     Application startup complete.
```
