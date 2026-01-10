# 🔧 Netlify 빌드 시 템플릿/정적 파일 복사 해결책

## 문제

Netlify Functions는 `netlify/functions/` 디렉토리만 패키징하므로, 프로젝트 루트의 `templates/`와 `static/` 디렉토리가 포함되지 않습니다.

## 해결 방법

### 빌드 시 파일 복사

`netlify.toml`의 `build.command`에서 빌드 시 템플릿과 정적 파일을 Functions 디렉토리로 복사합니다:

```toml
[build]
  command = "mkdir -p netlify/functions/templates netlify/functions/static && cp -r templates/* netlify/functions/templates/ 2>/dev/null || true && cp -r static/* netlify/functions/static/ 2>/dev/null || true"
```

### 경로 업데이트

`app/main.py`에서 다음 경로를 우선적으로 확인합니다:

1. `netlify/functions/templates` (빌드 시 복사됨)
2. 프로젝트 루트의 `templates`
3. 기타 fallback 경로

## 작동 방식

### 빌드 프로세스

1. Netlify가 빌드 시작
2. `build.command` 실행:
   - `netlify/functions/templates/` 디렉토리 생성
   - `netlify/functions/static/` 디렉토리 생성
   - `templates/*` → `netlify/functions/templates/` 복사
   - `static/*` → `netlify/functions/static/` 복사
3. Functions 패키징:
   - `netlify/functions/` 디렉토리 전체를 패키징
   - 이제 `templates/`와 `static/`이 포함됨

### 런타임 경로 해결

`app/main.py`는 다음 순서로 템플릿 디렉토리를 찾습니다:

1. `netlify/functions/templates` (Functions 패키지 내부)
2. 프로젝트 루트의 `templates`
3. 기타 fallback 경로

## 파일 구조

### 빌드 전
```
project-root/
├── templates/
├── static/
└── netlify/functions/
    ├── server.py
    └── requirements.txt
```

### 빌드 후 (Functions 패키지)
```
/var/task/
├── templates/          ← 복사됨
├── static/             ← 복사됨
├── server.py
└── requirements.txt
```

## 확인 방법

### 로컬에서 테스트
```bash
# 수동으로 파일 복사
mkdir -p netlify/functions/templates netlify/functions/static
cp -r templates/* netlify/functions/templates/
cp -r static/* netlify/functions/static/

# 확인
ls -la netlify/functions/templates/
ls -la netlify/functions/static/
```

### Health Check에서 확인
```bash
curl https://app-market-analytics.netlify.app/health
```

응답에서 확인:
- `files.templates`: 파일 목록 확인
- `template_dirs_checked`: 경로 확인

## 주의사항

### Git에 포함 여부

`netlify/functions/templates/`와 `netlify/functions/static/`은:
- `.gitignore`에 추가하면 안 됨
- 빌드 시마다 새로 복사되므로 Git에 포함할 필요는 없지만
- 디렉토리 구조는 유지해야 함 (`.gitkeep` 파일 포함)

### 빌드 시간

파일 복사로 인해 빌드 시간이 약간 증가할 수 있지만, 일반적으로 무시할 수 있는 수준입니다.

## 다음 단계

1. ✅ 빌드 명령어 설정 완료
2. ✅ 경로 업데이트 완료
3. ⏳ Netlify 배포 확인
4. ⏳ Health Check로 검증

## 변경사항 적용 완료

모든 변경사항이 GitHub에 푸시되었습니다. Netlify가 자동으로 다시 배포하며, 빌드 시 템플릿과 정적 파일이 Functions 패키지에 포함됩니다.
