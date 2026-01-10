# ⚠️ 긴급: Netlify Base Directory 오류 수정

## 🚨 현재 오류

```
Base directory does not exist: /opt/build/repo/Desktop/application/016-Application-market-analytics
```

## ✅ 즉시 해결 방법 (2분 안에)

### Step 1: Netlify 대시보드 열기
1. https://app.netlify.com 접속
2. **app-market-analytics** 사이트 클릭

### Step 2: Build Settings 수정
1. 왼쪽 메뉴: **Site settings**
2. **Build & deploy** 클릭
3. **Build settings** 섹션
4. **"Edit settings"** 버튼 클릭

### Step 3: Base directory 지우기 (가장 중요!)
1. **Base directory** 필드 찾기
2. **모든 텍스트 삭제** (완전히 비우기)
3. **Save** 클릭

### Step 4: 재배포
1. **Deploys** 탭으로 이동
2. **"Trigger deploy"** 클릭
3. **"Clear cache and deploy site"** 선택
4. 배포 완료 대기

## 📋 설정 확인표

배포 전에 다음을 확인하세요:

- [ ] Base directory: **(비워있어야 함)**
- [ ] Build command: `pip install -r requirements.txt`
- [ ] Publish directory: `.` 또는 비워두기
- [ ] Functions directory: `netlify/functions`

## 🎯 핵심 포인트

**Base directory를 비워야 배포가 성공합니다!**

프로젝트 파일들이 이미 GitHub 저장소 루트에 있으므로, Base directory 설정은 필요 없습니다.


