from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os
import sys
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
# 프로젝트 루트 찾기 - 여러 경우 고려
current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)

# Netlify Functions 환경: netlify/functions/server.py -> app/main.py
# 로컬 환경: app/main.py
# 프로젝트 루트 찾기 (app 디렉토리의 부모)
if current_dir.endswith("app"):
    project_root = os.path.dirname(current_dir)
else:
    # 다른 구조를 고려
    project_root = os.path.dirname(current_dir)

static_dir = os.path.join(project_root, "static")
templates_dir = os.path.join(project_root, "templates")

# 디렉토리 존재 확인 및 로깅
print(f"Current file: {current_file}")
print(f"Current dir: {current_dir}")
print(f"Project root: {project_root}")
print(f"Static dir exists: {os.path.exists(static_dir)} ({static_dir})")
print(f"Templates dir exists: {os.path.exists(templates_dir)} ({templates_dir})")

# 정적 파일 마운트
if os.path.exists(static_dir):
    try:
        app.mount("/static", StaticFiles(directory=static_dir), name="static")
        print(f"Static files mounted from: {static_dir}")
    except Exception as e:
        print(f"Error mounting static files: {e}")
else:
    print(f"Warning: Static directory not found at {static_dir}")

# 템플릿 디렉토리 설정 (Netlify Functions 환경 고려)
templates = None
possible_template_dirs = [
    templates_dir,  # 프로젝트 루트/templates
    os.path.join(current_dir, "..", "templates"),  # app/../templates
    os.path.join(project_root, "templates"),  # 재확인
    "templates",  # 상대 경로
    "/var/task/templates",  # Netlify Functions 기본 경로
]

for template_path in possible_template_dirs:
    abs_path = os.path.abspath(template_path) if not os.path.isabs(template_path) else template_path
    if os.path.exists(abs_path):
        try:
            templates = Jinja2Templates(directory=abs_path)
            print(f"Templates loaded from: {abs_path}")
            break
        except Exception as e:
            print(f"Error loading templates from {abs_path}: {e}")
            continue

if templates is None:
    # 최종 fallback: 현재 디렉토리 기준
    try:
        templates = Jinja2Templates(directory="templates")
        print("Templates loaded from default: templates (fallback)")
    except Exception as e:
        print(f"CRITICAL: Failed to load templates: {e}")
        # 빈 템플릿 객체로 초기화하여 앱이 시작되도록 함
        templates = Jinja2Templates(directory=os.getcwd())


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """메인 대시보드"""
    try:
        if templates is None:
            return HTMLResponse(content="<h1>템플릿을 로드할 수 없습니다. Functions 로그를 확인하세요.</h1>", status_code=500)
        return templates.TemplateResponse("dashboard.html", {"request": request})
    except Exception as e:
        print(f"Error rendering dashboard: {e}")
        return HTMLResponse(content=f"<h1>오류 발생: {str(e)}</h1>", status_code=500)


@app.get("/apps", response_class=HTMLResponse)
async def apps_page(request: Request):
    """앱 목록 페이지"""
    try:
        if templates is None:
            return HTMLResponse(content="<h1>템플릿을 로드할 수 없습니다.</h1>", status_code=500)
        return templates.TemplateResponse("apps.html", {"request": request})
    except Exception as e:
        print(f"Error rendering apps page: {e}")
        return HTMLResponse(content=f"<h1>오류 발생: {str(e)}</h1>", status_code=500)


@app.get("/analysis", response_class=HTMLResponse)
async def analysis_page(request: Request):
    """분석 페이지"""
    try:
        if templates is None:
            return HTMLResponse(content="<h1>템플릿을 로드할 수 없습니다.</h1>", status_code=500)
        return templates.TemplateResponse("analysis.html", {"request": request})
    except Exception as e:
        print(f"Error rendering analysis page: {e}")
        return HTMLResponse(content=f"<h1>오류 발생: {str(e)}</h1>", status_code=500)


@app.get("/report", response_class=HTMLResponse)
async def report_page(request: Request):
    """AI 리포트 페이지"""
    try:
        if templates is None:
            return HTMLResponse(content="<h1>템플릿을 로드할 수 없습니다.</h1>", status_code=500)
        return templates.TemplateResponse("report.html", {"request": request})
    except Exception as e:
        print(f"Error rendering report page: {e}")
        return HTMLResponse(content=f"<h1>오류 발생: {str(e)}</h1>", status_code=500)


@app.get("/health")
def health_check():
    """헬스 체크"""
    import os
    possible_paths = {
        "project_root": project_root,
        "static_dir": static_dir,
        "templates_dir": templates_dir,
        "current_dir": current_dir,
        "current_file": current_file
    }
    
    path_status = {}
    for name, path in possible_paths.items():
        path_status[name] = {
            "path": path,
            "exists": os.path.exists(path) if path else False
        }
    
    # 템플릿 디렉토리 확인
    template_dirs_to_check = [
        templates_dir,
        os.path.join(current_dir, "..", "templates"),
        os.path.join(project_root, "templates"),
        "templates",
        "/var/task/templates"
    ]
    
    template_status = []
    for td in template_dirs_to_check:
        abs_td = os.path.abspath(td) if td and not os.path.isabs(td) else td
        template_status.append({
            "path": abs_td,
            "exists": os.path.exists(abs_td) if abs_td else False
        })
    
    return {
        "status": "ok" if templates is not None else "error",
        "templates_loaded": templates is not None,
        "paths": path_status,
        "template_dirs_checked": template_status,
        "cwd": os.getcwd(),
        "sys_path": sys.path[:3] if 'sys' in dir() else []
    }

