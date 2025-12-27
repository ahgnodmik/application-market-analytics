# 🆕 새 Repository 설정 가이드

## 현재 상태 확인

프로젝트 파일들은 모두 준비되어 있습니다. GitHub 저장소만 새로 만들고 연결하면 됩니다.

## 1단계: Git 초기화

```bash
cd /Users/donghakim/Desktop/application/016-Application-market-analytics

# Git 초기화
git init

# 브랜치 이름 설정
git branch -M main
```

## 2단계: 파일 추가 및 커밋

```bash
# .gitignore 확인 (이미 설정되어 있음)
cat .gitignore

# 모든 파일 추가
git add .

# 첫 커밋
git commit -m "Initial commit: Application Market Analytics"
```

## 3단계: GitHub 저장소 생성

1. **https://github.com** 접속
2. **"New repository"** 클릭
3. 저장소 정보 입력:
   - **Repository name**: `app-market-analytics` (또는 원하는 이름)
   - **Description**: "안드로이드 마켓 분석기 - 구현 난이도가 낮고 시장성이 검증된 앱 타입 추출 서비스"
   - **Public** 또는 **Private** 선택
   - ⚠️ **"Add a README file"** 체크 해제
   - ⚠️ **"Add .gitignore"** 체크 해제 (이미 있음)
   - ⚠️ **"Choose a license"** 선택 안 함
4. **"Create repository"** 클릭

## 4단계: GitHub에 연결 및 푸시

GitHub에서 제공하는 명령어 사용 (HTTPS 권장):

```bash
# 원격 저장소 추가
git remote add origin https://github.com/your-username/app-market-analytics.git

# GitHub에 푸시
git push -u origin main
```

또는 SSH 사용 시:

```bash
git remote add origin git@github.com:your-username/app-market-analytics.git
git push -u origin main
```

## 5단계: Netlify에 연결

### 방법 1: Netlify 대시보드에서

1. **https://app.netlify.com** 접속
2. **"Add new site"** → **"Import an existing project"**
3. **GitHub** 선택
4. 저장소 선택 (`app-market-analytics`)
5. **"Connect"** 클릭

### 방법 2: Netlify CLI 사용

```bash
# 로그인 (아직 안 했다면)
netlify login

# 사이트 초기화
netlify init

# 선택 옵션:
# - "Create & configure a new site"
# - 사이트 이름: app-market-analytics
# - Build command: (Enter - netlify.toml에서 설정됨)
# - Publish directory: . (Enter)
```

## 6단계: 빌드 설정 확인

Netlify 대시보드에서:

- **Build command**: `pip install -r requirements.txt`
- **Publish directory**: `.` (또는 비워두기)
- **Functions directory**: `netlify/functions`
- **Base directory**: **(비워두기)** ⚠️ 매우 중요!

## 7단계: 환경 변수 설정

1. **Site settings** → **Environment variables**
2. **"Add a variable"** 클릭
3. 추가:
   - Key: `OPENAI_API_KEY`
   - Value: `your-api-key-here`
4. **"Save"** 클릭

## 8단계: 배포 확인

1. **"Deploy site"** 클릭
2. 배포 완료 대기
3. 제공된 URL로 접속 확인:
   - 예: `https://app-market-analytics.netlify.app`

## ✅ 완료 체크리스트

- [ ] Git 저장소 초기화
- [ ] 파일 커밋
- [ ] GitHub 저장소 생성
- [ ] GitHub에 푸시
- [ ] Netlify에 연결
- [ ] Base directory 비워두기 확인
- [ ] 환경 변수 설정
- [ ] 배포 성공 확인

## 🔍 문제 해결

### Git push 오류
```bash
# 원격 저장소 확인
git remote -v

# 원격 저장소 재설정
git remote remove origin
git remote add origin https://github.com/your-username/app-market-analytics.git
```

### Netlify 연결 오류
- GitHub 저장소가 Public인지 확인
- Netlify에 GitHub 권한이 있는지 확인

### 배포 오류
- Base directory가 비어있는지 확인
- Build command가 올바른지 확인
- Functions directory가 `netlify/functions`인지 확인

