# OpenAI API 키 설정 가이드

## 현재 상태

✅ API 키 파일은 존재합니다 (`.env.local`)
❌ API 키가 유효하지 않거나 만료되었습니다

## 해결 방법

### 1. 올바른 API 키 확인

1. [OpenAI Platform](https://platform.openai.com/account/api-keys)에 접속
2. 로그인 후 "API keys" 섹션으로 이동
3. 새 API 키 생성 또는 기존 키 확인
4. API 키는 `sk-`로 시작하는 긴 문자열입니다

### 2. API 키 설정

#### 방법 1: .env.local 파일 수정 (권장)
```bash
# .env.local 파일을 열어서 수정
nano .env.local
# 또는
open .env.local
```

다음 형식으로 저장:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

#### 방법 2: .env 파일 생성
```bash
echo "OPENAI_API_KEY=sk-your-actual-api-key-here" > .env
```

### 3. API 키 확인

설정 후 다음 명령어로 확인:
```bash
python3 check_api_key.py
```

성공 메시지가 나오면 정상입니다!

## 중요 사항

- ✅ API 키는 `sk-`로 시작해야 합니다
- ✅ 공백이나 따옴표 없이 직접 입력
- ✅ `.env.local` 또는 `.env` 파일에 저장
- ✅ API 키는 절대 공유하지 마세요
- ✅ 만료되거나 유효하지 않은 키는 401 오류 발생

## API 키 형식 예시

```
OPENAI_API_KEY=sk-proj-abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
```

## 문제 해결

### 401 오류 (Invalid API Key)
- API 키가 올바른지 확인
- OpenAI 계정에 충분한 크레딧이 있는지 확인
- API 키가 만료되지 않았는지 확인

### API 키를 찾을 수 없음
- `.env` 또는 `.env.local` 파일이 프로젝트 루트에 있는지 확인
- 파일 이름에 오타가 없는지 확인
- `OPENAI_API_KEY=` 형식이 올바른지 확인

## 테스트

API 키 설정 후 다음 명령어로 테스트:
```bash
python3 check_api_key.py
```

성공하면:
```
✅ API 키가 설정되어 있습니다
✅ OpenAI 클라이언트 생성 성공
✅ OpenAI API 연결 성공!
```



