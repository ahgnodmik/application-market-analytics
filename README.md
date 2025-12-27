# Application Market Analytics

안드로이드 마켓(Play Store) 상위 앱을 분석하여 **구현 난이도가 낮고 시장성이 검증된 앱 타입**을 추출하는 내부용 분석 서비스입니다.

## 기능

- 📱 앱 데이터 입력 및 CSV 업로드
- 🔧 기능 단위 분해 및 관리
- 📊 구현 난이도 자동 계산 (0~2점)
- 💰 시장성 신호 점수 자동 계산 (0~10점)
- 📈 2축 매트릭스 시각화
- 🎯 앱 타입 그룹화 및 추천
- 🤖 **ChatGPT 기반 AI 리포트 생성** (신규)
- 🎨 **Notion 스타일의 깔끔한 UI** (Tailwind CSS)

## 설치 및 실행

### 빠른 시작

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. 로컬 개발 서버 실행 (npm 사용 - 권장)
npm run dev

# 또는 Python 직접 실행
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 또는 실행 스크립트 사용
chmod +x run.sh
./run.sh
```

### Netlify 배포

```bash
# Netlify Functions 로컬 테스트
npm run netlify:dev

# 프로덕션 배포
npm run netlify:deploy:prod
```

### 브라우저 접속

서버 실행 후 브라우저에서 접속:
- **메인 대시보드**: http://localhost:8000
- **API 문서 (Swagger)**: http://localhost:8000/docs
- **앱 관리 페이지**: http://localhost:8000/apps
- **분석 페이지**: http://localhost:8000/analysis

## 사용 방법

1. 대시보드에서 앱 데이터 입력
2. 각 앱의 기능을 분해하여 입력
3. 자동으로 점수가 계산됨
4. 필터 조건 설정하여 후보 앱 타입 확인

## 필터링 조건

- 시장성 점수 ≥ 6
- 구현 난이도 ≤ 1.0
- 핵심 기능 수 ≤ 5

