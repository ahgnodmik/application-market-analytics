# 🚨 Netlify Functions 설정 완전 가이드

## 현재 문제

Functions가 전혀 감지되지 않습니다. 다음을 순서대로 확인하세요.

## 1단계: Netlify 대시보드 설정 확인

### Build settings 확인

1. Netlify 대시보드 접속
2. **Site settings** → **Build & deploy** → **Build settings**

**확인 사항:**
- ✅ **Base directory**: 비어있어야 함 (또는 프로젝트 루트)
- ✅ **Build command**: `netlify.toml`에서 가져오는지, 또는 수동 설정
- ✅ **Publish directory**: `.` (또는 올바른 경로)
- ✅ **Functions directory**: `netlify/functions` (또는 비어있음 - netlify.toml에서)

**중요:** Base directory가 잘못 설정되어 있으면 Functions를 찾을 수 없습니다!

### Functions settings 확인

1. **Site settings** → **Functions**
2. Python Functions가 활성화되어 있는지 확인
3. 런타임 버전 확인 (Python 3.10)

## 2단계: 빌드 로그 확인 (가장 중요!)

1. **Deploys** 탭 클릭
2. 최신 배포 클릭
3. **Build log** 전체 확인

**확인할 메시지:**
```
✅ "Installing dependencies"
✅ "Packaging Functions..."
✅ "Found 1 function(s)" 또는 "Found 2 function(s)"
❌ "No functions found"
❌ "Error packaging functions"
❌ "ModuleNotFoundError"
```

**빌드 로그가 비어있다면:**
- 빌드가 실행되지 않았을 수 있음
- GitHub webhook 문제일 수 있음
- Netlify와 GitHub 연결 확인 필요

## 3단계: 테스트 함수 확인

간단한 테스트 함수 `hello.py`를 추가했습니다.

**테스트 URL:**
```
https://app-market-analytics.netlify.app/.netlify/functions/hello
```

**예상 결과:**
- ✅ 200 OK + JSON → Functions 작동!
- ❌ 404 → Functions 배포 안됨

## 4단계: 파일 구조 확인

현재 구조:
```
netlify/functions/
├── hello.py              ← 파일 기반 함수 (테스트용)
├── server/
│   ├── handler.py        ← 디렉토리 기반 함수
│   ├── requirements.txt
│   └── __init__.py
└── requirements.txt      ← 루트 레벨 (선택사항)
```

## 가능한 원인 및 해결

### 원인 1: Base directory 설정 오류

**증상:** 빌드는 성공하지만 Functions가 없음

**해결:**
1. Site settings → Build & deploy
2. Base directory를 **비워두기** (빈 값)
3. 저장 후 재배포

### 원인 2: Python Functions 런타임 문제

**증상:** Functions가 감지되지만 실행 안됨

**해결:**
1. Site settings → Functions
2. Python 런타임 확인
3. 필요시 재설정

### 원인 3: 빌드 자체가 실행되지 않음

**증상:** Deploys 탭에 배포가 없음

**해결:**
1. GitHub와 Netlify 연결 확인
2. Webhook 확인
3. 수동으로 "Trigger deploy" 클릭

## 즉시 해야 할 것

1. **빌드 로그 확인** ← 가장 중요!
   - 전체 로그를 복사
   - Functions 관련 부분 확인

2. **Site settings 확인**
   - Base directory 확인
   - Build command 확인

3. **테스트 함수 확인**
   - `/.netlify/functions/hello` 접속
   - 결과 확인

4. **정보 공유**
   - 빌드 로그 (Functions 관련 부분)
   - Site settings 스크린샷
   - 테스트 함수 결과

**이 정보 없이는 정확한 진단이 불가능합니다!**
