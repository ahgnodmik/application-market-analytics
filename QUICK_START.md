# 🚀 빠른 시작 가이드

## 로컬 개발 (npm 사용)

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. 개발 서버 실행
npm run dev
```

브라우저에서 http://localhost:8000 접속

---

## Netlify 배포

### 자동 배포 (Git 연동)

1. GitHub에 코드 푸시
2. Netlify 대시보드에서 저장소 연결
3. 자동으로 배포됨

### 수동 배포

```bash
# 미리보기 배포
npm run netlify:deploy

# 프로덕션 배포
npm run netlify:deploy:prod
```

### 로컬에서 Netlify 환경 테스트

```bash
npm run netlify:dev
```

---

## 환경 변수 설정

### 로컬 개발

`.env.local` 파일 생성:

```env
OPENAI_API_KEY=your-api-key-here
```

### Netlify

대시보드 → Site settings → Environment variables → Add variable

---

## 사용 가능한 명령어

| 명령어 | 설명 |
|--------|------|
| `npm run dev` | 로컬 개발 서버 실행 |
| `npm run netlify:dev` | Netlify Functions 로컬 테스트 |
| `npm run netlify:deploy:prod` | Netlify 프로덕션 배포 |

---

## 배포된 사이트

- 사이트 이름: **app-market-analytics**
- URL: `https://app-market-analytics.netlify.app`


