# 🔧 Netlify Functions Python 의존성 설정

## Netlify Functions의 의존성 설치 방식

Netlify Functions (Python)는 각 함수 디렉토리에 있는 `requirements.txt` 파일을 자동으로 읽어서 설치합니다.

## 현재 설정

### 1. Functions 디렉토리 구조

```
netlify/
└── functions/
    ├── __init__.py
    ├── server.py          # 함수 엔트리 포인트
    └── requirements.txt   # ✅ 이 파일이 있어야 함
```

### 2. requirements.txt 위치

Netlify Functions는 `netlify/functions/requirements.txt` 파일을 자동으로 찾아서 설치합니다.

### 3. netlify.toml 설정

```toml
[build]
  # 빌드 명령어는 비워두거나 최소한으로 설정
  command = "echo 'Dependencies will be installed by Netlify Functions runtime'"
  functions = "netlify/functions"
  publish = "."
```

## ✅ 해결 방법

### 방법 1: Functions 디렉토리에 requirements.txt 복사 (권장)

이미 `netlify/functions/requirements.txt`를 생성했습니다.

### 방법 2: 심볼릭 링크 사용

```bash
cd netlify/functions
ln -s ../../requirements.txt requirements.txt
```

### 방법 3: Build command에서 복사

```toml
[build]
  command = "cp requirements.txt netlify/functions/requirements.txt"
  functions = "netlify/functions"
  publish = "."
```

## 🔍 확인

다음 명령어로 확인:

```bash
ls -la netlify/functions/requirements.txt
cat netlify/functions/requirements.txt
```

## 📝 중요 사항

1. **Functions 디렉토리의 requirements.txt**가 있어야 합니다
2. Build command에서 명시적으로 설치할 필요가 없습니다
3. Netlify가 런타임에 자동으로 설치합니다
4. 각 함수 디렉토리마다 별도의 requirements.txt를 가질 수 있습니다

## 🚀 배포

이제 Git에 푸시하면:

1. `netlify/functions/requirements.txt`가 배포됩니다
2. Netlify가 자동으로 의존성을 설치합니다
3. 함수가 정상적으로 실행됩니다


