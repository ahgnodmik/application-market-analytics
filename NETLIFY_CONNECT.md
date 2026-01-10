# 🔗 Netlify 연결 가이드

## ✅ GitHub 연결 완료

- 저장소: https://github.com/ahgnodmik/application-market-analytics.git
- 브랜치: main
- 코드 푸시 완료

## 🚀 Netlify 자동 배포 설정

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

**⚠️ Base directory를 반드시 비워두세요!**

| 설정 항목 | 값 |
|---------|-----|
| **Base directory** | **(비워두기 - 아무것도 입력하지 마세요)** ⚠️ |
| Build command | `pip install -r requirements.txt` |
| Publish directory | `.` (또는 비워두기) |
| Functions directory | `netlify/functions` |

### 5단계: 환경 변수 설정

1. **"Show advanced"** 클릭
2. **"New variable"** 클릭
3. 추가:
   - Key: `OPENAI_API_KEY`
   - Value: `your-api-key-here`
4. **"Save"** 클릭

### 6단계: 배포 시작

1. **"Deploy site"** 버튼 클릭
2. 배포 진행 상황 확인
3. 배포 완료 대기

## 🔄 자동 배포

설정 완료 후:
- ✅ `git push` 하면 자동으로 배포됩니다
- ✅ Pull Request 생성 시 미리보기 배포
- ✅ main 브랜치 푸시 시 프로덕션 배포

## 📍 배포된 사이트

배포 완료 후 Netlify가 제공하는 URL:
- 예: `https://app-market-analytics.netlify.app`
- 또는 사이트 이름에 따라 다른 URL

## ⚠️ 중요 사항

### Base directory 오류 방지

만약 Base directory 오류가 발생하면:

1. **Site settings** → **Build & deploy** → **Build settings**
2. **"Edit settings"** 클릭
3. **Base directory** 필드를 **완전히 비우기**
4. **Save** 클릭
5. **"Trigger deploy"** → **"Clear cache and deploy site"**

## ✅ 완료 체크리스트

- [x] GitHub 저장소 연결
- [x] 코드 푸시 완료
- [ ] Netlify에 저장소 연결
- [ ] Base directory 비워두기 확인
- [ ] 환경 변수 설정
- [ ] 첫 배포 성공
- [ ] 사이트 접속 확인


