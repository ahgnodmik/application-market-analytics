# 📊 카테고리별 순위 수집 및 GPT 분석 기능

## 기능 개요

1. **카테고리별 순위 수집**: Play Store 카테고리별로 상위 앱 가져오기
2. **GPT 분석**: 카테고리별 또는 다중 카테고리 비교 분석

## 새로운 API 엔드포인트

### 1. 카테고리 목록 조회

```bash
GET /api/playstore/categories
```

사용 가능한 Play Store 카테고리 목록 반환

### 2. 카테고리별 순위 가져오기

```bash
POST /api/playstore/fetch-by-category?play_category=APPLICATION_SOCIAL&limit=100&force=true
```

**파라미터:**
- `play_category`: 카테고리 이름 (예: "APPLICATION_SOCIAL", "GAME", "APPLICATION_PRODUCTIVITY")
- `category`: 순위 타입 ("top_free", "top_paid", "top_grossing")
- `limit`: 가져올 앱 수
- `force`: 월요일이 아니어도 강제 실행

### 3. 카테고리별 GPT 분석

```bash
POST /api/playstore/analyze-category?play_category=APPLICATION_SOCIAL&limit=50&force=true
```

**파라미터:**
- `play_category`: 분석할 카테고리
- `category`: 순위 타입
- `limit`: 분석할 앱 수
- `force`: 월요일이 아니어도 강제 실행

**응답:**
```json
{
  "success": true,
  "category": "APPLICATION_SOCIAL",
  "apps_analyzed": 50,
  "analysis": "GPT 분석 결과 텍스트...",
  "raw_apps": [...]
}
```

### 4. 다중 카테고리 비교 분석

```bash
POST /api/playstore/analyze-multiple-categories
Content-Type: application/json

{
  "categories": ["APPLICATION_SOCIAL", "APPLICATION_PRODUCTIVITY", "APPLICATION_ENTERTAINMENT"],
  "limit_per_category": 50,
  "ranking_type": "top_free"
}
```

**응답:**
```json
{
  "success": true,
  "categories_analyzed": ["APPLICATION_SOCIAL", "APPLICATION_PRODUCTIVITY", "APPLICATION_ENTERTAINMENT"],
  "analysis": "GPT 비교 분석 결과 텍스트...",
  "categories_data": {...}
}
```

## 사용 가능한 카테고리

### 게임 카테고리
- `GAME` - 모든 게임
- `GAME_ACTION` - 액션 게임
- `GAME_ADVENTURE` - 어드벤처 게임
- `GAME_CASUAL` - 캐주얼 게임
- `GAME_PUZZLE` - 퍼즐 게임
- 등등...

### 애플리케이션 카테고리
- `APPLICATION` - 모든 앱
- `APPLICATION_SOCIAL` - 소셜 앱
- `APPLICATION_PRODUCTIVITY` - 생산성 앱
- `APPLICATION_ENTERTAINMENT` - 엔터테인먼트 앱
- `APPLICATION_COMMUNICATION` - 커뮤니케이션 앱
- `APPLICATION_FINANCE` - 금융 앱
- 등등...

전체 카테고리 목록은 `/api/playstore/categories`로 확인 가능

## 사용 예시

### 1. 카테고리 목록 확인

```bash
curl "https://app-analytics.up.railway.app/api/playstore/categories"
```

### 2. 소셜 앱 카테고리 순위 가져오기

```bash
curl -X POST "https://app-analytics.up.railway.app/api/playstore/fetch-by-category?play_category=APPLICATION_SOCIAL&limit=50&force=true"
```

### 3. 소셜 앱 카테고리 GPT 분석

```bash
curl -X POST "https://app-analytics.up.railway.app/api/playstore/analyze-category?play_category=APPLICATION_SOCIAL&limit=50&force=true"
```

### 4. 여러 카테고리 비교 분석

```bash
curl -X POST "https://app-analytics.up.railway.app/api/playstore/analyze-multiple-categories" \
  -H "Content-Type: application/json" \
  -d '{
    "categories": ["APPLICATION_SOCIAL", "APPLICATION_PRODUCTIVITY"],
    "limit_per_category": 30,
    "ranking_type": "top_free"
  }'
```

## GPT 분석 내용

GPT가 제공하는 분석:

1. **카테고리 특성 분석**
   - 주요 트렌드
   - 사용자 니즈와 동기
   - 경쟁 강도

2. **성공 패턴 분석**
   - 높은 순위 앱들의 공통점
   - 평점과 리뷰 수의 관계
   - 무료 vs 유료 모델 분석

3. **기회 분석**
   - 시장 공백 (Gap)
   - 진입 가능성
   - 추천 앱 타입

4. **구체적인 추천**
   - 빠르게 구축 가능한 앱 아이디어 (최대 5개)
   - 각 아이디어의 핵심 기능 (3-5개)
   - 예상 구현 난이도 (0-2점)
   - 예상 시장성 점수 (0-10점)
   - 예상 화면 수
   - 예상 개발 기간

## 구현 파일

- `app/services/play_store_scraper_real.py`: 카테고리별 수집 기능
- `app/services/category_analyzer.py`: GPT 분석 기능
- `app/routers/playstore.py`: API 엔드포인트

## 다음 단계

1. Railway 배포 후 테스트
2. 카테고리별 데이터 수집 확인
3. GPT 분석 결과 확인
4. 프론트엔드 UI 추가 (선택사항)
