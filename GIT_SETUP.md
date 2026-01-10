# 📦 Git 설정 및 GitHub 푸시 가이드

## 1단계: Git 초기화 (아직 안 했다면)

```bash
cd /Users/donghakim/Desktop/application/016-Application-market-analytics

# Git 초기화
git init

# .gitignore 확인 (이미 설정되어 있음)
cat .gitignore
```

## 2단계: 파일 추가 및 커밋

```bash
# 모든 파일 추가
git add .

# 커밋
git commit -m "Initial commit: Application Market Analytics with Netlify deployment"
```

## 3단계: GitHub 저장소 생성

1. **https://github.com** 접속
2. **"New repository"** 클릭
3. 저장소 이름 입력 (예: `application-market-analytics`)
4. **Public** 또는 **Private** 선택
5. **"Create repository"** 클릭
6. **⚠️ README, .gitignore, license 추가하지 마세요** (이미 있음)

## 4단계: GitHub에 연결 및 푸시

```bash
# 원격 저장소 추가 (GitHub에서 제공하는 URL 사용)
git remote add origin https://github.com/your-username/your-repo-name.git

# 브랜치 이름을 main으로 설정
git branch -M main

# GitHub에 푸시
git push -u origin main
```

## 5단계: Netlify에서 연결

1. **https://app.netlify.com** 접속
2. **"Add new site"** → **"Import an existing project"**
3. **GitHub** 선택
4. 저장소 선택
5. **"Connect"** 클릭
6. 빌드 설정 확인 (자동으로 `netlify.toml` 읽음)
7. **"Deploy site"** 클릭

## ✅ 완료!

이제 Git에 푸시할 때마다 자동으로 Netlify에 배포됩니다!


