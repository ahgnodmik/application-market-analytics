# 🎯 최종 설정 가이드 (새 Repository)

## ✅ 현재 상태

모든 필수 파일이 준비되어 있습니다:
- ✅ netlify.toml
- ✅ package.json  
- ✅ requirements.txt
- ✅ netlify/functions/server.py
- ✅ app/ 디렉토리
- ✅ templates/ 디렉토리
- ✅ static/ 디렉토리

## 🚀 설정 단계

### 1단계: 기존 원격 저장소 제거

```bash
cd /Users/donghakim/Desktop/application/016-Application-market-analytics

# 기존 원격 저장소 제거
git remote remove origin
```

### 2단계: GitHub에 새 저장소 생성

1. **https://github.com** 접속
2. **"New repository"** 클릭
3. 입력:
   - **Repository name**: `app-market-analytics`
   - **Description**: "안드로이드 마켓 분석기"
   - **Public** 또는 **Private** 선택
   - ⚠️ **Add README** 체크 해제
   - ⚠️ **Add .gitignore** 체크 해제  
   - ⚠️ **Choose a license** 선택 안 함
4. **"Create repository"** 클릭

### 3단계: 새 원격 저장소 연결

```bash
# 원격 저장소 추가 (YOUR_USERNAME을 실제 GitHub 사용자명으로 변경)
git remote add origin https://github.com/YOUR_USERNAME/app-market-analytics.git

# 확인
git remote -v
```

### 4단계: 파일 커밋 및 푸시

```bash
# 모든 파일 추가
git add .

# 커밋
git commit -m "Initial commit: Application Market Analytics"

# GitHub에 푸시
git push -u origin main
```

### 5단계: Netlify 연결

1. **https://app.netlify.com** 접속
2. **"Add new site"** → **"Import an existing project"**
3. **GitHub** 선택
4. `app-market-analytics` 저장소 선택
5. **"Connect"** 클릭

### 6단계: 빌드 설정 (매우 중요!)

**⚠️ Base directory를 반드시 비워두세요!**

- **Build command**: `pip install -r requirements.txt`
- **Publish directory**: `.`
- **Functions directory**: `netlify/functions`
- **Base directory**: **(비워두기 - 아무것도 입력하지 마세요)**

### 7단계: 환경 변수 설정

1. **Site settings** → **Environment variables**
2. **"Add a variable"** 클릭
3. 추가:
   - Key: `OPENAI_API_KEY`
   - Value: `your-api-key-here`
4. **"Save"** 클릭

### 8단계: 배포

1. **"Deploy site"** 클릭
2. 배포 완료 대기
3. 제공된 URL로 접속:
   - 예: `https://app-market-analytics.netlify.app`

## 📋 빠른 명령어 모음

```bash
# 1. 원격 저장소 제거
git remote remove origin

# 2. 새 원격 저장소 추가 (YOUR_USERNAME 변경 필요)
git remote add origin https://github.com/YOUR_USERNAME/app-market-analytics.git

# 3. 파일 커밋 및 푸시
git add .
git commit -m "Initial commit: Application Market Analytics"
git push -u origin main
```

## ✅ 체크리스트

- [ ] GitHub에 새 저장소 생성 (`app-market-analytics`)
- [ ] 기존 원격 저장소 제거
- [ ] 새 원격 저장소 연결
- [ ] 파일 커밋 및 푸시
- [ ] Netlify에 저장소 연결
- [ ] Base directory 비워두기 확인
- [ ] 환경 변수 설정
- [ ] 배포 성공 확인

## 🎉 완료!

모든 설정이 완료되면:
- 로컬 개발: `npm run dev`
- Netlify 배포: 자동 (Git push 시)
- 사이트 URL: `https://app-market-analytics.netlify.app`


