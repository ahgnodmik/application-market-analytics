# 📋 Repository 상태 확인 및 재설정

## 현재 상태

✅ **프로젝트 파일**: 모두 준비됨
- netlify.toml ✅
- package.json ✅
- requirements.txt ✅
- netlify/functions/ ✅

## 다음 단계

### 1. GitHub에 새 저장소 생성

1. **https://github.com** 접속
2. **"New repository"** 클릭
3. 저장소 정보:
   - **Name**: `app-market-analytics`
   - **Description**: "안드로이드 마켓 분석기"
   - **Public** 또는 **Private** 선택
   - ⚠️ **README, .gitignore, license 추가하지 마세요**
4. **"Create repository"** 클릭

### 2. 원격 저장소 연결

터미널에서 실행:

```bash
cd /Users/donghakim/Desktop/application/016-Application-market-analytics

# 기존 원격 저장소 제거 (있다면)
git remote remove origin

# 새 원격 저장소 추가
git remote add origin https://github.com/your-username/app-market-analytics.git

# 원격 저장소 확인
git remote -v
```

### 3. 파일 커밋 및 푸시

```bash
# 변경사항 확인
git status

# 모든 변경사항 추가
git add .

# 커밋
git commit -m "Initial commit: Application Market Analytics"

# GitHub에 푸시
git push -u origin main
```

### 4. Netlify 연결

1. **https://app.netlify.com** 접속
2. **"Add new site"** → **"Import an existing project"**
3. **GitHub** 선택
4. `app-market-analytics` 저장소 선택
5. **"Connect"** 클릭

### 5. 빌드 설정 (매우 중요!)

**Base directory를 비워두기:**

- Build command: `pip install -r requirements.txt`
- Publish directory: `.`
- Functions directory: `netlify/functions`
- **Base directory: (비워두기)** ⚠️

### 6. 환경 변수 설정

- Site settings → Environment variables
- `OPENAI_API_KEY` 추가

### 7. 배포

- "Deploy site" 클릭
- 배포 완료 대기

## ✅ 준비된 파일들

모든 필수 파일이 준비되어 있습니다:

- ✅ `netlify.toml` - Netlify 설정
- ✅ `package.json` - npm 스크립트
- ✅ `requirements.txt` - Python 의존성
- ✅ `netlify/functions/server.py` - 서버리스 함수
- ✅ `.gitignore` - Git 제외 파일
- ✅ `app/` - FastAPI 애플리케이션
- ✅ `templates/` - HTML 템플릿
- ✅ `static/` - 정적 파일

## 🎯 빠른 명령어

```bash
# 1. 원격 저장소 제거 및 재추가
git remote remove origin
git remote add origin https://github.com/your-username/app-market-analytics.git

# 2. 파일 커밋 및 푸시
git add .
git commit -m "Initial commit: Application Market Analytics"
git push -u origin main
```

그 다음 Netlify 대시보드에서 저장소 연결하면 됩니다!


