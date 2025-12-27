# 🚀 Netlify 자동 배포 설정 가이드

## ✅ GitHub 연결 완료

- 저장소: https://github.com/ahgnodmik/application-market-analytics.git
- 브랜치: main

## 📋 Netlify 자동 배포 설정

### 1단계: Netlify 대시보드 접속

1. **https://app.netlify.com** 접속
2. 로그인 (GitHub 계정 권장)

### 2단계: 새 사이트 생성

1. **"Add new site"** 버튼 클릭
2. **"Import an existing project"** 선택
3. **GitHub** 선택

### 3단계: 저장소 선택

1. GitHub 저장소 목록에서 **`application-market-analytics`** 선택
2. **"Connect"** 클릭

### 4단계: 빌드 설정 (매우 중요!)

Netlify가 자동으로 `netlify.toml`을 읽지만, 다음을 확인하세요:

| 설정 항목 | 값 |
|---------|-----|
| **Base directory** | **(비워두기)** ⚠️ 매우 중요! |
| Build command | `pip install -r requirements.txt` |
| Publish directory | `.` (또는 비워두기) |
| Functions directory | `netlify/functions` |

**⚠️ Base directory를 반드시 비워두세요!**

### 5단계: 환경 변수 설정

1. **"Show advanced"** 클릭 (또는 배포 후 Site settings에서)
2. **"New variable"** 클릭
3. 추가:
   - Key: `OPENAI_API_KEY`
   - Value: `your-api-key-here`
4. **"Save"** 클릭

### 6단계: 배포 시작

1. **"Deploy site"** 버튼 클릭
2. 배포 진행 상황 확인
3. 배포 완료 대기 (약 2-3분)

### 7단계: 배포 확인

배포가 완료되면:
- Netlify가 제공하는 URL 확인
- 예: `https://app-market-analytics.netlify.app`
- 또는 사이트 이름에 따라 다른 URL

## 🔄 자동 배포 작동 방식

이제부터:
- ✅ Git에 `git push` 하면 자동으로 배포됩니다
- ✅ Pull Request 생성 시 미리보기 배포가 생성됩니다
- ✅ main 브랜치에 푸시하면 프로덕션 배포가 실행됩니다

## 📝 배포 확인 방법

### Netlify 대시보드에서

1. **Deploys** 탭
2. 최신 배포 상태 확인
3. **Functions** 탭에서 서버리스 함수 로그 확인

### 사이트 접속

- 메인: `https://your-site.netlify.app/`
- 대시보드: `https://your-site.netlify.app/`
- 앱 관리: `https://your-site.netlify.app/apps`
- 분석: `https://your-site.netlify.app/analysis`
- AI 리포트: `https://your-site.netlify.app/report`

## ⚠️ 문제 해결

### Base directory 오류

만약 여전히 Base directory 오류가 발생하면:

1. **Site settings** → **Build & deploy** → **Build settings**
2. **"Edit settings"** 클릭
3. **Base directory** 필드를 **완전히 비우기**
4. **Save** 클릭
5. **"Trigger deploy"** → **"Clear cache and deploy site"**

### 빌드 실패

1. **Deploys** → 최신 배포 → **Build log** 확인
2. 오류 메시지 확인
3. 필요시 `requirements.txt` 확인

### 함수 실행 오류

1. **Functions** → **Logs** 확인
2. 환경 변수가 올바르게 설정되었는지 확인

## ✅ 완료 체크리스트

- [ ] GitHub 저장소 연결 완료
- [ ] Netlify에 저장소 연결
- [ ] Base directory 비워두기 확인
- [ ] 환경 변수 설정 (`OPENAI_API_KEY`)
- [ ] 첫 배포 성공
- [ ] 사이트 접속 확인
- [ ] 자동 배포 작동 확인 (Git push 테스트)

## 🎉 완료!

이제 Git에 푸시할 때마다 자동으로 Netlify에 배포됩니다!

