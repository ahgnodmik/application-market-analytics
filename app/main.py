from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from app.database import engine, Base
from app.routers import apps, analysis, upload, report

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Application Market Analytics", version="1.0.0")

# 라우터 등록
app.include_router(apps.router)
app.include_router(analysis.router)
app.include_router(upload.router)
app.include_router(report.router)

# 정적 파일 및 템플릿
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

