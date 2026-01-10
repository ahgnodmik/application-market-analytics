from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os
from app.database import engine, Base
from app.routers import apps, analysis, upload, report

# 데이터베이스 테이블 생성 (Netlify Functions 환경에서도 안전하게)
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    # Netlify Functions 환경에서 실패할 수 있음 (읽기 전용 파일 시스템)
    # 이 경우 메모리 DB로 fallback하거나 외부 DB 사용 권장
    print(f"Warning: Database initialization failed: {e}")

app = FastAPI(title="Application Market Analytics", version="1.0.0")

# 라우터 등록
app.include_router(apps.router)
app.include_router(analysis.router)
app.include_router(upload.router)
app.include_router(report.router)

# 정적 파일 및 템플릿 경로 (Netlify Functions 환경 고려)
# 프로젝트 루트 찾기
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))

static_dir = os.path.join(project_root, "static")
templates_dir = os.path.join(project_root, "templates")

# 디렉토리가 존재하는 경우에만 마운트
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
if os.path.exists(templates_dir):
    templates = Jinja2Templates(directory=templates_dir)
else:
    # Fallback: 상대 경로
    app.mount("/static", StaticFiles(directory="static"), name="static")
    templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """메인 대시보드"""
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/apps", response_class=HTMLResponse)
async def apps_page(request: Request):
    """앱 목록 페이지"""
    return templates.TemplateResponse("apps.html", {"request": request})


@app.get("/analysis", response_class=HTMLResponse)
async def analysis_page(request: Request):
    """분석 페이지"""
    return templates.TemplateResponse("analysis.html", {"request": request})


@app.get("/report", response_class=HTMLResponse)
async def report_page(request: Request):
    """AI 리포트 페이지"""
    return templates.TemplateResponse("report.html", {"request": request})


@app.get("/health")
def health_check():
    """헬스 체크"""
    return {"status": "ok"}

