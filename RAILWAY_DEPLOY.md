# Railway 배포 가이드

## Railway 배포 방법

Railway는 Git 기반 자동 배포를 사용합니다. 환경 변수를 변경하거나 Git에 push하면 자동으로 재배포됩니다.

## 방법 1: Railway Variables에서 API 키 설정 (권장)

### 1단계: Railway 대시보드 접속

1. https://railway.app 접속
2. 로그인
3. 프로젝트 선택 (`app-analytics` 또는 해당 프로젝트)

### 2단계: Variables 탭으로 이동

1. 왼쪽 메뉴에서 **"Variables"** 클릭
2. 또는 상단의 **"Variables"** 탭 클릭

### 3단계: API 키 추가/수정

#### 기존 키가 있는 경우:
1. `OPENAI_API_KEY` 찾기
2. 오른쪽 **"Edit"** 클릭 (또는 연필 아이콘)
3. **Value** 필드에 새 API 키 붙여넣기
4. **"Save"** 또는 **"Update"** 클릭

#### 새로 추가하는 경우:
1. **"+ New Variable"** 또는 **"+ Add Variable"** 클릭
2. **Key**: `OPENAI_API_KEY` 입력
3. **Value**: API 키 전체 붙여넣기
   - `.env.local` 파일의 값 복사 (앞뒤 공백 제거)
4. **"Add"** 클릭

### 4단계: 자동 재배포 확인

- Railway가 **자동으로 재배포를 시작**합니다
- Variables 변경 시 자동 재배포가 트리거됩니다
- "Deployments" 탭에서 배포 상태 확인
- 배포 완료 대기 (약 1-2분)

## 방법 2: Git Push로 배포 (코드 변경 시)

### 1단계: 변경사항 확인

```bash
git status
```

### 2단계: 변경사항 커밋 (필요한 경우)

```bash
git add .
git commit -m "Update: Set OpenAI API key in Railway"
```

### 3단계: Git Push

```bash
git push origin main
```

### 4단계: Railway 자동 배포 확인

1. Railway 대시보드 → "Deployments" 탭
2. 새로운 배포가 시작되는지 확인
3. 배포 완료 대기

## ⚠️ 중요: .env.local은 로컬용입니다

`.env.local` 파일은 **로컬 개발 환경**에서만 사용됩니다.

- ✅ **로컬 개발**: `.env.local` 파일 사용
- ✅ **Railway 배포**: Railway Variables에 직접 설정
- ❌ `.env.local` 파일을 Git에 커밋하지 마세요 (보안)

## 배포 상태 확인

### Railway 대시보드

1. **"Deployments"** 탭 클릭
2. 최신 배포 확인:
   - ✅ **"Active"** - 배포 완료
   - 🔄 **"Building"** - 배포 중
   - ❌ **"Failed"** - 배포 실패 (로그 확인)

### 로그 확인

1. "Deployments" 탭 → 최신 배포 선택
2. **"View Logs"** 클릭
3. 다음 메시지 확인:
   - `✅ All modules imported successfully`
   - `✅ FastAPI application started successfully`
   - OpenAI 관련 에러가 없는지 확인

## 테스트

배포 완료 후:

1. 웹사이트 접속: https://app-analytics.up.railway.app
2. 카테고리 분석 페이지로 이동
3. 카테고리 선택 후 "GPT 분석 시작" 클릭
4. 401 에러 없이 정상 작동하는지 확인

## 문제 해결

### 배포가 실패하는 경우

1. **로그 확인**: Deployments → View Logs
2. **일반적인 원인**:
   - Python 패키지 설치 실패
   - 데이터베이스 연결 오류
   - 환경 변수 누락

### API 키가 작동하지 않는 경우

1. Railway Variables에서 키 확인
2. API 키가 전체 복사되었는지 확인 (공백 없음)
3. Railway 재배포 확인
4. Railway 로그에서 에러 메시지 확인

## 빠른 참조

- Railway 대시보드: https://railway.app
- 프로젝트 URL: https://app-analytics.up.railway.app
- OpenAI API 키 생성: https://platform.openai.com/api-keys
