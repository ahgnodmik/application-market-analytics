# 🔧 Netlify 빌드 오류 최종 수정

## 문제 진단

Netlify Functions의 구조가 잘못되었을 수 있습니다. 더 간단한 구조로 변경했습니다.

## 수정된 구조

### 현재 구조 (단순화) ✅

```
netlify/
└── functions/
    ├── __init__.py
    ├── server.py          ← 함수 엔트리 포인트
    └── requirements.txt   ← 의존성 (Netlify가 자동 설치)
```

### 함수 등록 방식

Netlify Functions는:
- `netlify/functions/server.py` 파일을 `server` 함수로 인식
- `netlify/functions/requirements.txt`를 자동으로 감지하여 설치
- 파일 이름이 함수 이름이 됩니다 (`server`)

## netlify.toml 설정

```toml
[build]
  command = "python3 --version && pip3 --version || echo 'Python/pip check'"
  functions = "netlify/functions"
  publish = "."

[[redirects]]
  from = "/*"
  to = "/.netlify/functions/server"
  status = 200
  force = true
```

## 확인 사항

### 1. 파일 구조 확인

```bash
ls -la netlify/functions/
```

다음 파일들이 있어야 합니다:
- ✅ `server.py`
- ✅ `requirements.txt`
- ✅ `__init__.py` (선택사항)

### 2. server.py 확인

`handler` 변수가 export되어 있는지 확인:
```python
handler = Mangum(app, lifespan="off")
```

### 3. Netlify 대시보드 확인

1. **Deploys** → 최신 배포 확인
2. **Functions** → `server` 함수 확인
3. **Functions Logs** → 의존성 설치 로그 확인

## 가능한 문제 및 해결

### 문제 1: 의존성 설치 실패

**확인:**
- `netlify/functions/requirements.txt` 파일이 있는지
- 모든 패키지 이름과 버전이 올바른지

**해결:**
- requirements.txt 파일 확인
- 패키지 버전 조정

### 문제 2: 함수를 찾을 수 없음

**확인:**
- `netlify/functions/server.py` 파일 존재
- `handler` 변수가 정의되어 있는지

**해결:**
- 파일 위치 확인
- handler 변수 확인

### 문제 3: 경로 오류

**확인:**
- `server.py`에서 프로젝트 루트 경로가 올바른지
- `app.main` 모듈을 import할 수 있는지

**해결:**
- sys.path 설정 확인
- 프로젝트 구조 확인

## ✅ 변경사항 적용

변경사항을 GitHub에 푸시했습니다. Netlify가 자동으로 다시 배포합니다.

## 다음 단계

1. **Netlify 대시보드 확인**
   - Deploys → 최신 배포 상태
   - Functions → server 함수 상태

2. **빌드 로그 확인**
   - Deploys → 최신 배포 → Build log
   - 오류 메시지 확인

3. **Functions 로그 확인**
   - Functions → server → Logs
   - 실행 시 오류 확인

## 디버깅 명령어

로컬에서 테스트:

```bash
# Netlify Functions 로컬 테스트
netlify dev

# 또는
npm run netlify:dev
```
