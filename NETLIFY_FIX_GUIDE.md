# 🔧 Netlify Base Directory 오류 해결 가이드

## 🚨 현재 오류

```
Base directory does not exist: /opt/build/repo/Desktop/application/016-Application-market-analytics
```

## ✅ 해결 방법

### 방법 1: Netlify 대시보드에서 수정 (추천)

1. **Netlify 대시보드 접속**
   - https://app.netlify.com
   - 사이트 선택 (현재: shotsmaker - 이름 변경 권장: application-market-analytics)

2. **Build 설정 수정**
   - **Site settings** 클릭
   - **Build & deploy** → **Build settings**
   - **"Edit settings"** 버튼 클릭

3. **Base directory 제거**
   - **Base directory** 필드를 찾아서
   - **완전히 비워두기** (빈 값으로)
   - **Save** 클릭

4. **다시 배포**
   - **Deploys** 탭으로 이동
   - **"Trigger deploy"** → **"Clear cache and deploy site"** 클릭

### 방법 2: 빌드 설정 확인

다음 설정들이 올바른지 확인하세요:

| 설정 항목 | 값 |
|---------|-----|
| Build command | `pip install -r requirements.txt` |
| Publish directory | `.` (또는 비워두기) |
| Functions directory | `netlify/functions` |
| **Base directory** | **(비워두기)** ⚠️ |

## 📁 프로젝트 구조 확인

GitHub 저장소의 파일들이 **루트 디렉토리**에 있는지 확인:

```
shotsmaker/          ← 저장소 루트
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── ...
├── netlify/
│   └── functions/
│       └── server.py
├── templates/
├── static/
├── netlify.toml     ← 이 파일이 루트에 있어야 함
├── requirements.txt
└── package.json
```

## 🔍 확인 방법

### GitHub에서 확인
1. https://github.com/ahgnodmik/shotsmaker 접속
2. 파일들이 루트에 있는지 확인
3. `netlify.toml` 파일이 보이는지 확인

### 로컬에서 확인
```bash
cd /Users/donghakim/Desktop/application/016-Application-market-analytics

# 현재 디렉토리의 파일 확인
ls -la

# netlify.toml이 있는지 확인
cat netlify.toml

# Git 상태 확인
git status
```

## ⚡ 빠른 해결 체크리스트

- [ ] Netlify 대시보드 → Site settings → Build & deploy
- [ ] Base directory 필드 **비우기**
- [ ] Save 클릭
- [ ] Deploys → Trigger deploy → Clear cache and deploy site
- [ ] 배포 완료 대기

## 💡 참고

- Netlify는 기본적으로 저장소 **루트**에서 빌드를 시작합니다
- Base directory는 **하위 디렉토리에 프로젝트가 있을 때만** 사용합니다
- 이 프로젝트는 루트에 있어야 하므로 Base directory는 **비워야 합니다**

## 🆘 여전히 안 되면

1. **빌드 로그 확인**
   - Deploys → 최신 배포 → Build log

2. **GitHub 저장소 구조 재확인**
   - 모든 파일이 루트에 있는지 확인

3. **Git 푸시 확인**
   ```bash
   git add .
   git commit -m "Fix: Remove base directory from Netlify settings"
   git push
   ```

