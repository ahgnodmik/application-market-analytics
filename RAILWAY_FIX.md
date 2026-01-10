# 🔧 Railway uvicorn 에러 수정

## 문제

Railway 배포 시 `uvicorn: command not found` 에러 발생

## 원인

Railway에서 `uvicorn` 명령이 PATH에 없거나, 설치된 패키지가 제대로 인식되지 않음

## 해결 방법

### 수정 사항

1. **Procfile 수정**
   ```diff
   - web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   + web: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

2. **railway.json 수정**
   ```diff
   - "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
   + "startCommand": "python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT"
   ```

3. **runtime.txt 추가** (Python 버전 명시)
   ```
   python-3.10
   ```

## 변경 사항 적용

변경사항이 푸시되면 Railway가 자동으로 재배포합니다.

### 수동 재배포

Railway 대시보드에서:
1. 프로젝트 선택
2. "Deployments" 탭
3. "Redeploy" 클릭

## 확인

배포 완료 후:
- 로그에서 `uvicorn` 에러가 사라졌는지 확인
- 서비스가 정상 시작되는지 확인
