# 🔧 웹페이지 작동 불가 문제 해결

## 문제

빌드는 성공했지만 웹페이지가 작동하지 않습니다.

## 원인

### 1. SQLite 데이터베이스 문제 (주요 원인)

Netlify Functions는 **읽기 전용 파일 시스템**을 사용합니다:
- 프로젝트 디렉토리에 파일을 쓸 수 없음
- SQLite 파일(`market_analytics.db`)을 생성할 수 없음
- `Base.metadata.create_all()`이 실패할 수 있음

### 2. 정적 파일 및 템플릿 경로 문제

Netlify Functions 환경에서 상대 경로가 다를 수 있습니다.

## 해결 방법

### 1. SQLite 데이터베이스 수정

`app/database.py` 수정:
- Netlify Functions 환경에서는 `/tmp` 디렉토리 사용
- `/tmp` 디렉토리는 쓰기 가능하지만 함수 실행 간에 유지되지 않음 (임시 해결책)
- 최종 해결책: 외부 데이터베이스 사용 (PostgreSQL, MongoDB 등)

### 2. 데이터베이스 초기화 예외 처리

`app/main.py` 수정:
- `Base.metadata.create_all()`을 try-except로 감싸서 실패 시에도 앱이 시작되도록 함

### 3. 정적 파일 및 템플릿 경로 수정

`app/main.py` 수정:
- 프로젝트 루트를 동적으로 찾아서 경로 설정
- Netlify Functions 환경에서도 올바른 경로 사용

## 변경 사항

### app/database.py
```python
# Netlify Functions 환경 확인
if os.path.exists("/tmp") and not DATABASE_URL.startswith("sqlite:///:memory:"):
    # Netlify Functions 환경: /tmp 디렉토리 사용
    db_path = "/tmp/market_analytics.db"
    DATABASE_URL = f"sqlite:///{db_path}"
```

### app/main.py
```python
# 데이터베이스 초기화 예외 처리
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Warning: Database initialization failed: {e}")

# 정적 파일 및 템플릿 경로 (프로젝트 루트 기준)
project_root = os.path.abspath(os.path.join(current_dir, ".."))
static_dir = os.path.join(project_root, "static")
templates_dir = os.path.join(project_root, "templates")
```

## ⚠️ 중요 제한사항

### SQLite의 한계

`/tmp` 디렉토리를 사용하더라도:
- ✅ 함수 실행 중에는 데이터를 저장할 수 있음
- ❌ 함수 실행 간에 데이터가 유지되지 않음
- ❌ 각 함수 호출마다 새로운 데이터베이스 파일이 생성됨

### 권장 해결책

**프로덕션 환경에서는 외부 데이터베이스 사용을 권장합니다:**

1. **Supabase** (무료 PostgreSQL)
   - https://supabase.com
   - 무료 플랜 제공
   - PostgreSQL 호환

2. **MongoDB Atlas** (무료 MongoDB)
   - https://www.mongodb.com/cloud/atlas
   - 무료 플랜 제공
   - NoSQL 데이터베이스

3. **Railway** (PostgreSQL 호스팅)
   - https://railway.app
   - 쉬운 설정
   - PostgreSQL 제공

### 환경 변수 설정

Netlify 대시보드에서 환경 변수 설정:
1. Site settings → Environment variables
2. `DATABASE_URL` 추가:
   ```
   DATABASE_URL=postgresql://user:password@host:port/database
   ```

## ✅ 변경사항 적용

변경사항을 GitHub에 푸시했습니다. Netlify가 자동으로 다시 배포합니다.

## 다음 단계

1. **배포 확인**
   - Netlify 대시보드 → Deploys → 최신 배포 확인
   - Functions → server → Logs에서 오류 확인

2. **웹사이트 테스트**
   - 메인 페이지: `https://your-site.netlify.app/`
   - API 엔드포인트: `https://your-site.netlify.app/api/apps/`
   - 헬스 체크: `https://your-site.netlify.app/health`

3. **Functions 로그 확인**
   - Netlify 대시보드 → Functions → server → Logs
   - 데이터베이스 초기화 오류가 있는지 확인
   - 경로 관련 오류가 있는지 확인

## 임시 해결책 vs 최종 해결책

### 현재 (임시 해결책)
- `/tmp` 디렉토리 사용
- 데이터가 유지되지 않음
- 기본 기능 테스트 가능

### 권장 (최종 해결책)
- 외부 데이터베이스 사용 (Supabase, MongoDB Atlas 등)
- 데이터 영구 저장
- 프로덕션 환경에 적합
