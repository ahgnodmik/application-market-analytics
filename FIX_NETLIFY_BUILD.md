# 🔧 Netlify 빌드 오류 해결

## 오류 메시지
```
Failed during stage 'Install dependencies': dependency_installation script returned non-zero exit code: 1
```

## 해결 방법

### 1. netlify.toml 빌드 명령어 확인

현재 설정:
```toml
[build]
  command = "pip install --upgrade pip && pip install -r requirements.txt"
```

### 2. 가능한 해결책

#### 방법 1: 빌드 명령어 수정 (권장)

Netlify 대시보드에서:

1. **Site settings** → **Build & deploy** → **Build settings**
2. **"Edit settings"** 클릭
3. **Build command** 필드 수정:
   ```
   pip install --upgrade pip && pip install -r requirements.txt
   ```
4. **Save** 클릭
5. **"Trigger deploy"** → **"Clear cache and deploy site"**

#### 방법 2: requirements.txt 확인

일부 패키지가 문제를 일으킬 수 있습니다. 필요시 버전을 조정:

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
pandas==2.1.3
python-multipart==0.0.6
jinja2==3.1.2
aiofiles==23.2.1
openai==1.3.0
python-dotenv==1.0.0
httpx==0.25.0
mangum==0.17.0
```

#### 방법 3: Python 버전 확인

`runtime.txt` 파일 확인:
```
python-3.9
```

Netlify 대시보드에서도 Python 3.9로 설정되었는지 확인.

### 3. 빌드 로그 확인

Netlify 대시보드에서:
1. **Deploys** → 최신 배포 클릭
2. **Build log** 확인
3. 정확한 오류 메시지 확인

### 4. 일반적인 문제 해결

#### pandas 설치 오류
pandas가 문제를 일으킬 수 있습니다. 필요시:
- pandas 버전 다운그레이드
- 또는 빌드 시간 증가 (더 많은 메모리 할당)

#### 메모리 부족
Netlify Functions 기본 메모리: 128MB
- 일부 패키지는 더 많은 메모리가 필요할 수 있습니다

#### 타임아웃
빌드 시간이 너무 오래 걸리는 경우:
- 불필요한 패키지 제거
- 빌드 캐시 활용

## ✅ 확인 체크리스트

- [ ] Build command가 올바른지 확인
- [ ] Python 버전이 3.9로 설정되었는지 확인
- [ ] requirements.txt에 모든 패키지가 포함되어 있는지 확인
- [ ] 빌드 로그에서 정확한 오류 메시지 확인
- [ ] Base directory가 비어있는지 확인

## 🔍 추가 디버깅

빌드 로그에서 다음을 확인하세요:
- 어떤 패키지 설치에서 실패했는지
- 정확한 오류 메시지
- Python 버전
- pip 버전


