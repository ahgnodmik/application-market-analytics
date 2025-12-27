# 📁 Netlify Functions 구조 수정

## 문제

Netlify Functions의 의존성 설치가 실패했습니다.

## 해결 방법

Netlify Python Functions는 각 함수가 **자신의 디렉토리**에 있어야 하며, 그 디렉토리에 `requirements.txt`가 있어야 합니다.

## 수정된 구조

### 이전 구조 (잘못됨)
```
netlify/
└── functions/
    ├── server.py
    └── requirements.txt  ❌
```

### 새로운 구조 (올바름) ✅
```
netlify/
└── functions/
    └── server/
        ├── __init__.py
        ├── server.py
        └── requirements.txt  ✅
```

## 작동 원리

1. `netlify/functions/server/` 디렉토리가 하나의 함수를 나타냅니다
2. 함수 이름은 디렉토리 이름입니다: `server`
3. `server/requirements.txt`가 있으면 Netlify가 자동으로 의존성을 설치합니다
4. `server/server.py`가 함수의 엔트리 포인트입니다

## netlify.toml 설정

```toml
[build]
  command = ""  # 빌드 명령어 없음 - Functions가 자동 처리
  functions = "netlify/functions"
  publish = "."

[[redirects]]
  from = "/*"
  to = "/.netlify/functions/server"  # server 함수로 라우팅
  status = 200
  force = true
```

## ✅ 확인

- [x] `netlify/functions/server/` 디렉토리 생성
- [x] `server.py`를 `server/` 디렉토리로 이동
- [x] `server/requirements.txt` 생성
- [x] `server/__init__.py` 생성
- [x] `netlify.toml` 업데이트

## 배포

변경사항이 푸시되면 Netlify가 자동으로:
1. `server/requirements.txt`를 감지
2. 의존성을 설치
3. `server/server.py`를 함수로 등록
4. 모든 요청을 `/functions/server`로 라우팅

