# 🔧 pip 명령어 오류 해결

## 오류 메시지

```
Command failed with exit code 127: pip install -r requirements.txt
zsh: command not found: pip
```

## 원인

- `pip` 명령어가 PATH에 없거나 직접 사용할 수 없습니다
- Exit code 127 = "command not found"

## 해결 방법

### netlify.toml 수정 완료

빌드 명령어를 `python -m pip`로 변경했습니다:

```toml
[build]
  command = "python -m pip install --upgrade pip && python -m pip install -r requirements.txt"
```

### 대안 (필요시)

Netlify에서 Python 3.9가 기본인 경우:

```toml
[build]
  command = "python3.9 -m pip install --upgrade pip && python3.9 -m pip install -r requirements.txt"
```

또는:

```toml
[build]
  command = "pip3 install --upgrade pip && pip3 install -r requirements.txt"
```

## 로컬 개발에서도 동일하게 사용

```bash
# 로컬에서도 python3 -m pip 사용
python3 -m pip install -r requirements.txt
```

## ✅ 확인

변경사항을 푸시하면 Netlify에서 자동으로 다시 배포됩니다:

```bash
git add netlify.toml
git commit -m "Fix: Use python -m pip instead of pip command"
git push
```


