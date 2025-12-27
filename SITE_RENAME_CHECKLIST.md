# ✅ Netlify 사이트 이름 변경 체크리스트

## 현재 상태
- ❌ 잘못된 이름: `shotsmaker`
- ✅ 올바른 이름: `application-market-analytics` (또는 원하는 이름)

## 변경 단계

### 1. Netlify 대시보드에서 이름 변경

1. **https://app.netlify.com** 접속
2. **shotsmaker** 사이트 선택
3. **Site settings** → **General** → **Site details**
4. **Site name** 필드 수정:
   ```
   shotsmaker → application-market-analytics
   ```
5. **Save** 클릭

### 2. 새 URL 확인

변경 후 새로운 URL이 생성됩니다:
- 기존: `https://shotsmaker.netlify.app`
- 신규: `https://application-market-analytics.netlify.app`

### 3. 환경 변수 확인

- Site settings → Environment variables
- 모든 환경 변수가 유지되는지 확인
- `OPENAI_API_KEY` 등 설정 확인

### 4. 배포 확인

- Deploys 탭에서 최신 배포 확인
- 새 URL로 접속 테스트
- 기능 정상 작동 확인

## 참고 사항

- ✅ 사이트 이름 변경은 설정에 영향을 주지 않습니다
- ✅ 환경 변수는 그대로 유지됩니다
- ✅ 배포 히스토리는 유지됩니다
- ⚠️ 기존 URL은 자동으로 새 URL로 리다이렉트될 수 있습니다 (하지만 새 URL 사용 권장)

## 권장 사이트 이름

프로젝트에 맞는 이름 선택:

1. **`application-market-analytics`** (추천)
   - 명확하고 설명적
   - 프로젝트 목적과 일치

2. **`app-market-analytics`**
   - 더 짧고 간결
   - 여전히 명확함

3. **`android-market-analysis`**
   - Android 마켓 분석임을 명확히 표시

