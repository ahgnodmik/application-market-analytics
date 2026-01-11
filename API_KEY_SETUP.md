# OpenAI API 키 설정 가이드

## 문제

GPT 분석 기능이 작동하지 않는 경우, OpenAI API 키가 설정되지 않았거나 유효하지 않을 수 있습니다.

### 일반적인 에러 메시지

- `Error code: 401` - API 키가 유효하지 않음
- `Incorrect API key provided` - 잘못된 API 키
- `invalid_api_key` - API 키 형식 오류

## 로컬 개발 환경

### 1. API 키 확인

```bash
python3 check_api_key.py
```

### 2. API 키 설정

프로젝트 루트에 `.env` 파일을 생성하고 다음 내용을 추가하세요:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

또는 `.env.local` 파일에 설정할 수도 있습니다.

### 3. API 키 가져오기

1. https://platform.openai.com/api-keys 접속
2. 계정 로그인
3. "Create new secret key" 클릭
4. 생성된 키를 복사하여 `.env` 파일에 붙여넣기

## Railway 배포 환경

### 1. Railway 대시보드 접속

1. https://railway.app 접속
2. 프로젝트 선택
3. "Variables" 탭 클릭

### 2. 환경 변수 추가

- **Key**: `OPENAI_API_KEY`
- **Value**: 실제 OpenAI API 키 (sk-로 시작)

### 3. 재배포

환경 변수를 추가한 후, Railway가 자동으로 재배포합니다.

## 확인 방법

### 로컬

```bash
python3 check_api_key.py
```

### Railway

Railway 로그에서 다음 메시지를 확인하세요:
- `OpenAI API key not found` - API 키가 설정되지 않음
- `OpenAI service not available` - OpenAI 서비스 사용 불가
- `Error code: 401` - API 키가 유효하지 않음

## 참고

- API 키는 절대 Git에 커밋하지 마세요 (`.env` 파일은 `.gitignore`에 포함되어 있습니다)
- Railway에서는 환경 변수로 설정해야 합니다
- API 키를 변경한 후에는 애플리케이션을 재시작해야 합니다
