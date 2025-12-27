# 설정 가이드

## OpenAI API 키 설정 (AI 리포트 기능 사용 시)

1. `.env` 파일을 프로젝트 루트에 생성합니다:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

2. OpenAI API 키는 [OpenAI Platform](https://platform.openai.com/api-keys)에서 발급받을 수 있습니다.

3. API 키 없이도 기본 기능(앱 관리, 분석, 추천)은 모두 사용 가능합니다.
   AI 리포트 기능만 사용하려면 API 키가 필요합니다.

## 의존성 설치

```bash
pip install -r requirements.txt
```

새로 추가된 패키지:
- `openai`: ChatGPT API 연동
- `python-dotenv`: 환경 변수 관리
- `httpx`: HTTP 클라이언트

## 실행

```bash
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 기능 확인

1. 기본 기능 (API 키 불필요)
   - 앱 추가/관리
   - 기능 분해
   - 점수 계산
   - 매트릭스 분석
   - 추천 앱 타입

2. AI 리포트 (API 키 필요)
   - 전체 앱 마켓 분석
   - 카테고리별 트렌드 분석
   - 구현 가능 앱 타입 추천
   - 시장 기회 분석




