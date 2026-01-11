# Railway OpenAI API 키 수정 가이드

## 현재 문제

에러 메시지:
```
Error code: 401 - Incorrect API key provided
```

이것은 Railway에 설정된 OpenAI API 키가 **유효하지 않거나 잘못되었음**을 의미합니다.

## 해결 방법

### 1단계: OpenAI에서 새 API 키 생성

1. https://platform.openai.com/api-keys 접속
2. 로그인 (OpenAI 계정 필요)
3. "Create new secret key" 클릭
4. 키 이름 입력 (예: "railway-production")
5. **생성된 키를 즉시 복사** (한 번만 표시됨!)
   - 형식: `sk-proj-...` (길고 복잡한 문자열)

### 2단계: Railway에 API 키 설정

1. Railway 대시보드 접속: https://railway.app
2. 프로젝트 선택 (`app-analytics` 또는 해당 프로젝트)
3. 왼쪽 메뉴에서 **"Variables"** 클릭
4. `OPENAI_API_KEY` 찾기
   - 있으면: "Edit" 클릭
   - 없으면: "+ New Variable" 클릭

5. 값 설정:
   - **Key**: `OPENAI_API_KEY`
   - **Value**: 복사한 API 키 전체 (예: `sk-proj-...`)
   - ✅ **"Add"** 또는 **"Update"** 클릭

### 3단계: 재배포 확인

1. Railway가 자동으로 재배포를 시작합니다
2. "Deployments" 탭에서 배포 상태 확인
3. 배포 완료 대기 (약 1-2분)

### 4단계: 테스트

1. 웹사이트 접속: https://app-analytics.up.railway.app
2. 카테고리 분석 페이지로 이동
3. 카테고리를 선택하고 "GPT 분석 시작" 클릭
4. 정상 작동 확인

## 주의사항

⚠️ **API 키 보안**
- API 키는 절대 Git에 커밋하지 마세요
- API 키는 공유하지 마세요
- 유출된 키는 즉시 삭제하고 새로 생성하세요

⚠️ **API 키 형식**
- 올바른 형식: `sk-proj-...` (매우 긴 문자열)
- 잘못된 형식: `sk-proj-...PeEA` (일부만 복사됨)
- API 키 전체를 복사해야 합니다

⚠️ **API 키 만료**
- OpenAI API 키는 만료되지 않지만, 삭제할 수 있습니다
- 키를 삭제하면 새 키를 생성해야 합니다

## 문제 해결

### 여전히 401 에러가 발생하는 경우

1. **API 키 확인**
   - Railway Variables에서 키가 정확히 복사되었는지 확인
   - 공백이나 줄바꿈이 포함되지 않았는지 확인

2. **새 API 키 생성**
   - 기존 키가 손상되었을 수 있으므로 새로 생성

3. **Railway 재배포**
   - Variables 변경 후 재배포가 완료되었는지 확인

4. **OpenAI 계정 확인**
   - OpenAI 계정에 충전이 되어 있는지 확인
   - API 사용량 제한을 초과하지 않았는지 확인

### 다른 에러 메시지

- `Error code: 429` - API 사용량 한도 초과 (과금 확인 필요)
- `Error code: 500` - OpenAI 서버 오류 (일시적, 재시도)
- `Error code: 503` - OpenAI 서비스 중단 (잠시 후 재시도)

## 추가 도움말

- OpenAI API 문서: https://platform.openai.com/docs
- Railway 문서: https://docs.railway.app
- 문제가 지속되면 Railway 로그 확인: Deployments → View Logs
