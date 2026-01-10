# 🔧 Netlify Base Directory 오류 해결

## 오류 메시지
```
Base directory does not exist: /opt/build/repo/Desktop/application/016-Application-market-analytics
```

## 원인
Netlify 대시보드에서 Base directory가 잘못 설정되어 있습니다.

## 해결 방법

### 1단계: Netlify 대시보드에서 Base Directory 제거

1. **https://app.netlify.com** 접속
2. 사이트 선택 (shotsmaker)
3. **Site settings** → **Build & deploy** → **Build settings**
4. **"Edit settings"** 클릭
5. **Base directory** 필드 확인:
   - ❌ 현재: `Desktop/application/016-Application-market-analytics`
   - ✅ 변경: **비워두기** (빈 값)
6. **"Save"** 클릭

### 2단계: 빌드 설정 확인

다음 설정들이 올바른지 확인:

- **Build command**: `pip install -r requirements.txt`
- **Publish directory**: `.` (또는 비워두기)
- **Functions directory**: `netlify/functions`
- **Base directory**: (비워두기)

### 3단계: 다시 배포

1. **Deploys** 탭으로 이동
2. **"Trigger deploy"** → **"Clear cache and deploy site"** 클릭

또는 Git에 새 커밋을 푸시하면 자동으로 다시 배포됩니다.

## ✅ 확인 사항

프로젝트 파일들이 GitHub 저장소의 **루트 디렉토리**에 있는지 확인:

```
shotsmaker/
├── app/
├── netlify/
├── templates/
├── static/
├── netlify.toml
├── requirements.txt
├── package.json
└── ...
```

만약 하위 디렉토리에 있다면, 해당 경로를 Base directory에 설정해야 하지만, 일반적으로는 루트에 두는 것이 좋습니다.

## 대안: GitHub 저장소 구조 확인

만약 프로젝트가 GitHub의 하위 디렉토리에 있다면:

1. GitHub 저장소 구조 확인
2. Base directory에 올바른 경로 설정
3. 또는 프로젝트 파일들을 저장소 루트로 이동

## 빠른 해결

**가장 간단한 방법:**
1. Netlify 대시보드 → Site settings → Build & deploy
2. Base directory 필드를 **완전히 비워두기**
3. Save
4. 다시 배포


