# 🚨 Netlify Base Directory 오류 해결

## 오류 메시지
```
Base directory does not exist: /opt/build/repo/Desktop/application/016-Application-market-analytics
```

## ⚠️ 원인
Netlify 대시보드의 Build settings에서 Base directory가 잘못 설정되어 있습니다.

## ✅ 해결 방법 (즉시 조치 필요)

### 1단계: Netlify 대시보드 접속

1. **https://app.netlify.com** 접속
2. **app-market-analytics** 사이트 선택
3. **Site settings** 클릭 (왼쪽 메뉴)

### 2단계: Build 설정 수정

1. **Build & deploy** 클릭
2. **Build settings** 섹션에서 **"Edit settings"** 버튼 클릭

### 3단계: Base directory 제거 (중요!)

**Base directory** 필드를 찾아서:
- ❌ 현재 값: `Desktop/application/016-Application-market-analytics` (또는 다른 경로)
- ✅ 변경: **완전히 비워두기** (빈 값으로)

다른 필드들도 확인:
- **Build command**: `pip install -r requirements.txt`
- **Publish directory**: `.` (또는 비워두기)
- **Functions directory**: `netlify/functions`
- **Base directory**: **(비워두기)** ⚠️

### 4단계: 저장 및 재배포

1. **"Save"** 버튼 클릭
2. **"Deploys"** 탭으로 이동
3. **"Trigger deploy"** → **"Clear cache and deploy site"** 클릭

## 📸 스크린샷 가이드

Build settings 화면에서:

```
┌─────────────────────────────────────┐
│ Build settings                      │
├─────────────────────────────────────┤
│ Build command:                      │
│ ┌─────────────────────────────────┐ │
│ │ pip install -r requirements.txt │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Publish directory:                  │
│ ┌─────────────────────────────────┐ │
│ │ .                               │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Functions directory:                │
│ ┌─────────────────────────────────┐ │
│ │ netlify/functions               │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Base directory:                     │
│ ┌─────────────────────────────────┐ │
│ │ [비워두기 - 아무것도 입력하지 않음]│ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

## 🔍 확인 방법

### GitHub 저장소 구조 확인

프로젝트 파일들이 **저장소 루트**에 있어야 합니다:

```
shotsmaker/  (또는 your-repo-name/)
├── app/
├── netlify/
│   └── functions/
│       └── server.py
├── templates/
├── static/
├── netlify.toml     ← 루트에 있어야 함
├── requirements.txt
├── package.json
└── ...
```

### 로컬에서 확인

```bash
cd /Users/donghakim/Desktop/application/016-Application-market-analytics

# netlify.toml이 루트에 있는지 확인
ls -la netlify.toml

# Git 상태 확인
git status
```

## ✅ 완료 체크리스트

- [ ] Netlify 대시보드 접속
- [ ] Site settings → Build & deploy → Build settings
- [ ] Base directory 필드 **완전히 비우기**
- [ ] Save 클릭
- [ ] Deploys → Trigger deploy → Clear cache and deploy site
- [ ] 배포 성공 확인

## 💡 왜 Base directory를 비워야 하나요?

- Netlify는 기본적으로 **저장소 루트**에서 빌드를 시작합니다
- 프로젝트 파일들이 이미 루트에 있으므로 Base directory는 **필요 없습니다**
- Base directory는 하위 디렉토리에 프로젝트가 있을 때만 사용합니다

## 🆘 여전히 안 되면

1. **GitHub 저장소 확인**
   - 모든 파일이 루트에 있는지 확인
   - `netlify.toml` 파일이 루트에 있는지 확인

2. **새로 푸시**
   ```bash
   git add .
   git commit -m "Fix: Ensure files are in repository root"
   git push
   ```

3. **Netlify 설정 재확인**
   - Base directory가 비어있는지 다시 확인
   - Build command가 올바른지 확인


