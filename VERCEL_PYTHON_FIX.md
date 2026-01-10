# 🔧 Vercel Python 버전 문제 해결

## 문제

Vercel의 최신 빌드 시스템(`uv`)이 `pyproject.toml`의 `[project]` 섹션을 요구합니다.

## 해결 방법

### 1. 올바른 `pyproject.toml` 생성

```toml
[project]
name = "application-market-analytics"
version = "1.0.0"
description = "Android Play Store App Market Analytics"
requires-python = ">=3.10,<3.13"
dependencies = [
    "fastapi==0.104.1",
    # ... 모든 의존성
]

[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"
```

### 2. `.python-version` 파일

```
3.10
```

### 3. `requirements.txt` 유지

Vercel은 두 가지 모두 지원하지만, 최신 버전은 `pyproject.toml`을 우선 사용합니다.

## 변경 사항

- ✅ `pyproject.toml` 추가 (올바른 형식)
- ✅ `.python-version` 확인 (3.10)
- ✅ `requirements.txt` 유지 (호환성)

## 다음 배포

이제 Vercel이 다음을 수행합니다:
1. `.python-version`에서 Python 3.10 확인
2. `pyproject.toml`에서 의존성 설치
3. `api/index.py`를 Function으로 배포
