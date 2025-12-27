# 실행 방법

## 빠른 시작

### 방법 1: 실행 스크립트 사용

```bash
./run.sh
```

### 방법 2: 수동 실행

1. **의존성 설치**
   ```bash
   pip install -r requirements.txt
   ```

2. **서버 실행**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **브라우저에서 접속**
   ```
   http://localhost:8000
   ```

## API 문서

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 사용 방법

1. **대시보드** (http://localhost:8000)
   - 전체 통계 확인
   - 추천 앱 타입 미리보기

2. **앱 관리** (http://localhost:8000/apps)
   - 앱 데이터 입력
   - CSV 파일 업로드
   - 각 앱의 기능 분해 및 입력

3. **분석** (http://localhost:8000/analysis)
   - 2축 매트릭스 시각화
   - 필터 조건 설정
   - 추천 앱 타입 목록 확인

## CSV 업로드 형식

CSV 파일 형식 예시:

```csv
name,category,rating,review_count,price_model,last_update,description
체크리스트 앱,생산성,4.5,150000,free,2024-01-15,일상 할일을 관리하는 앱
습관 추적기,생활,4.7,250000,subscription,2024-02-01,daily habit tracker
```

## 문제 해결

- **포트가 이미 사용 중인 경우**: `--port` 옵션으로 다른 포트 사용
  ```bash
  uvicorn app.main:app --reload --port 8001
  ```

- **모듈을 찾을 수 없는 경우**: 가상환경 활성화 확인 또는 `pip install -r requirements.txt` 재실행




