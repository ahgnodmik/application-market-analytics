# 📍 Netlify Base Directory 설정 가이드

## Base Directory란?

Base directory는 Netlify가 프로젝트의 루트를 어디로 인식할지 결정합니다.

## 중요: 현재 프로젝트의 경우

**Base directory는 비어있어야 합니다!** (빈 값)

이유:
- 프로젝트 루트가 이미 Git 저장소의 루트입니다
- Functions는 `netlify/functions/`에 있으므로 추가 경로가 필요 없습니다

## 설정 방법 (단계별)

### 방법 1: Netlify 대시보드에서 설정

1. **Netlify 대시보드 접속**
   ```
   https://app.netlify.com
   ```

2. **사이트 선택**
   - `app-market-analytics` 사이트 클릭

3. **Site settings 이동**
   - 왼쪽 메뉴에서 **"Site settings"** 클릭
   - 또는 상단의 **"Site configuration"** 클릭

4. **Build & deploy 메뉴**
   - 왼쪽 메뉴에서 **"Build & deploy"** 클릭
   - 하위 메뉴에서 **"Build settings"** 클릭

5. **Base directory 확인 및 수정**
   - 페이지 중간 부분의 **"Build settings"** 섹션 확인
   - **"Base directory"** 필드 찾기
   - 필드에 값이 있다면 → **모두 삭제** (비워두기)
   - 필드가 비어있다면 → 그대로 유지

6. **저장**
   - 페이지 하단 또는 상단의 **"Save"** 버튼 클릭

7. **재배포**
   - **"Trigger deploy"** → **"Deploy site"** 클릭
   - 또는 새로운 커밋을 푸시하면 자동 배포됨

### 방법 2: 스크린샷으로 위치 확인

**Build settings 페이지에서 찾을 위치:**
```
Site settings
└── Build & deploy
    └── Build settings
        ├── Build command: (여기)
        ├── Publish directory: (여기)
        ├── Base directory: ← 여기 확인!
        └── Functions directory: (여기)
```

## 올바른 설정 값

### 현재 프로젝트 (올바름) ✅

```
Base directory: (비어있음 - 빈 값)
Build command: (netlify.toml에서 가져옴)
Publish directory: .
Functions directory: (비어있음 또는 netlify/functions)
```

### 잘못된 설정 예시 ❌

```
Base directory: /Desktop/application/016-Application-market-analytics
Base directory: netlify
Base directory: app
```

## Base Directory가 잘못 설정되면?

**증상:**
- ❌ Functions가 감지되지 않음
- ❌ "No functions deployed" 메시지
- ❌ 404 에러
- ❌ 빌드는 성공하지만 Functions 없음

**이유:**
- Netlify가 잘못된 경로에서 Functions를 찾음
- `netlify/functions/` 디렉토리를 찾지 못함

## 확인 방법

### 1. 대시보드에서 확인

Site settings → Build & deploy → Build settings:
- Base directory 필드가 비어있는지 확인

### 2. 빌드 로그에서 확인

Deploys → 최신 배포 → Build log:
- 빌드 시작 경로 확인
- Functions 패키징 메시지 확인

### 3. 테스트 함수로 확인

배포 후:
```
https://app-market-analytics.netlify.app/.netlify/functions/test
```

- ✅ 200 OK → Base directory 올바름
- ❌ 404 → Base directory 확인 필요

## 현재 프로젝트 설정 요약

```
✅ Base directory: (비어있어야 함)
✅ Build command: (netlify.toml에서 자동 설정)
✅ Publish directory: . (netlify.toml에서 설정)
✅ Functions directory: netlify/functions (netlify.toml에서 설정)
```

## 문제 해결

### Base directory를 비운 후에도 문제가 있나요?

1. **캐시 클리어**
   - Site settings → Build & deploy → Build settings
   - "Clear cache and deploy site" 클릭

2. **수동 배포**
   - "Trigger deploy" → "Deploy site" 클릭

3. **빌드 로그 확인**
   - Deploys → 최신 배포 → Build log
   - Functions 관련 메시지 확인

## 참고

- Base directory는 선택 사항입니다
- 대부분의 프로젝트는 비워두는 것이 맞습니다
- 서브 디렉토리에 프로젝트가 있는 경우만 설정합니다
- 예: 모노레포에서 특정 앱만 배포할 때
