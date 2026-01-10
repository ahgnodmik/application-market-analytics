# 🔍 Netlify Functions 배포 확인 가이드

## 현재 구조 (올바름)

```
netlify/functions/
├── server/
│   ├── server.py          ✅ (handler 변수 export)
│   └── requirements.txt   ✅
├── app/                   ← 빌드 시 복사됨
├── templates/             ← 빌드 시 복사됨
└── static/                ← 빌드 시 복사됨
```

## 확인 방법

### 1. Netlify 대시보드 - Functions 탭

1. Netlify 대시보드 접속
2. **Functions** 탭 클릭
3. `server` 함수가 목록에 있는지 확인

**예상 결과:**
- ✅ `server` 함수가 목록에 있음 → Functions 배포됨
- ❌ 목록이 비어있음 → Functions 배포 안됨 (빌드 로그 확인)

### 2. Functions 직접 테스트

브라우저 또는 curl로 다음 URL 테스트:

```
https://app-market-analytics.netlify.app/.netlify/functions/server/health
```

**예상 결과:**
- ✅ 200 OK + JSON 응답 → Functions 정상 작동
- ❌ 404 Not Found → Functions가 배포되지 않음
- ❌ 500 Error → Functions 로그 확인 필요

### 3. Functions 로그 확인

Netlify 대시보드 → **Functions** → **server** → **Logs**

**정상 작동 시:**
```
[Server] ✅ Using app from functions directory
[Server] ✅ FastAPI app imported successfully
[Server] ✅ Mangum handler created successfully
```

**문제 발생 시:**
```
[Server] ❌ CRITICAL ERROR importing app: ...
```

### 4. 빌드 로그 확인

Netlify 대시보드 → **Deploys** → 최신 배포 → **Build log**

확인 사항:
- ✅ "Installing dependencies from requirements.txt" 메시지
- ✅ "Packaging Functions..." 메시지
- ❌ "Function server not found" 에러
- ❌ "ModuleNotFoundError" 에러

## 문제 해결

### 문제 1: Functions가 목록에 없음

**원인:** Functions 구조 문제 또는 requirements.txt 위치 문제

**해결:**
1. `netlify/functions/server/requirements.txt` 파일 존재 확인
2. `netlify/functions/server/server.py` 파일 존재 확인
3. `server.py`에서 `handler` 변수가 정의되어 있는지 확인

### 문제 2: Functions는 있지만 404 반환

**원인:** redirects 설정 문제

**해결:**
1. `netlify.toml`의 redirects 설정 확인:
   ```toml
   [[redirects]]
     from = "/*"
     to = "/.netlify/functions/server"
     status = 200
     force = true
   ```
2. `_redirects` 파일이 있으면 삭제 (netlify.toml이 우선)

### 문제 3: Functions는 작동하지만 앱이 500 에러

**원인:** 의존성 또는 경로 문제

**해결:**
1. Functions 로그 확인
2. `requirements.txt`에 모든 의존성 포함 확인
3. 경로 해석 로직 확인

## 변경사항 적용 완료

✅ 중복 파일(`handler.py`) 삭제
✅ 경로 해석 수정 (`functions_root` 올바르게 계산)
✅ 모든 변경사항 푸시 완료

**2-3분 후 위 확인 방법을 따라 테스트해주세요!**

## 중요한 체크리스트

- [ ] Functions 탭에서 `server` 함수 확인
- [ ] `/.netlify/functions/server/health` 직접 테스트
- [ ] Functions 로그에서 `[Server] ✅` 메시지 확인
- [ ] 빌드 로그에서 Functions 패키징 확인
- [ ] 메인 페이지(`/`) 접속 테스트

**여전히 404라면 위 체크리스트 결과를 공유해주세요!**
