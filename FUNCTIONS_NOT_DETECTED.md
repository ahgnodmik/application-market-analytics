# 🚨 Netlify Functions가 감지되지 않는 문제 해결

## 문제

Netlify 대시보드의 Functions 탭에 함수가 표시되지 않습니다.

## 가능한 원인 및 해결

### 1. Python Functions 구조 문제

Netlify Python Functions는 다음 구조를 요구합니다:

```
netlify/functions/
└── server/
    ├── __init__.py      ✅ (Python 패키지 인식)
    ├── handler.py       ✅ (엔트리 포인트)
    └── requirements.txt ✅ (의존성)
```

### 2. Git에 포함 여부 확인

Functions 파일들이 Git에 포함되어 있는지 확인:

```bash
git ls-files netlify/functions/
```

모든 파일이 표시되어야 합니다.

### 3. 빌드 로그 확인

Netlify 대시보드 → **Deploys** → 최신 배포 → **Build log**:

확인할 메시지:
- ✅ "Packaging Functions..." 
- ✅ "Found 1 function(s)"
- ❌ "No functions found"
- ❌ "Error packaging functions"

### 4. netlify.toml 설정 확인

```toml
[build]
  functions = "netlify/functions"  # 올바른 경로
```

### 5. Functions 직접 테스트

빌드 완료 후:

```
https://app-market-analytics.netlify.app/.netlify/functions/server/health
```

## 수정 사항

✅ `netlify/functions/server/__init__.py` 추가
✅ 빌드 명령어 개선 (완료 메시지 추가)
✅ 모든 파일 Git에 포함 확인

## 다음 단계

1. **배포 대기** (2-3분)
   - Netlify가 자동으로 재배포합니다

2. **빌드 로그 확인**
   - Deploys → 최신 배포 → Build log
   - "Packaging Functions..." 메시지 확인
   - 에러 메시지 확인

3. **Functions 탭 확인**
   - Functions 탭 새로고침
   - `server` 함수가 표시되는지 확인

4. **Functions 직접 URL 테스트**
   ```
   https://app-market-analytics.netlify.app/.netlify/functions/server/health
   ```

## 여전히 문제가 있다면

다음을 공유해주세요:

1. **빌드 로그** (Functions 관련 부분)
   - "Packaging Functions..." 메시지 유무
   - 에러 메시지

2. **Functions 탭 스크린샷**
   - 함수 목록이 비어있는지 확인

3. **Git 파일 목록**
   ```bash
   git ls-files netlify/functions/
   ```

## 추가 참고

Netlify Python Functions는:
- 각 함수는 디렉토리여야 함
- 디렉토리 이름 = 함수 이름
- `handler.py` 파일 필수
- `requirements.txt` 파일 필수
- `__init__.py` 권장 (Python 패키지 인식)
