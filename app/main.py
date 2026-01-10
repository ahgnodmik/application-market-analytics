from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
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

# Lambda/Netlify Functions 환경에서의 경로 확인
LAMBDA_TASK_ROOT = os.environ.get('LAMBDA_TASK_ROOT', '')
if LAMBDA_TASK_ROOT:
    project_root = LAMBDA_TASK_ROOT

static_dir = os.path.join(project_root, "static")
templates_dir = os.path.join(project_root, "templates")

# 디렉토리 존재 확인 및 로깅
print(f"[APP INIT] Current file: {current_file}")
print(f"[APP INIT] Current dir: {current_dir}")
print(f"[APP INIT] Project root: {project_root}")
print(f"[APP INIT] LAMBDA_TASK_ROOT: {LAMBDA_TASK_ROOT}")
print(f"[APP INIT] Static dir: {static_dir} (exists: {os.path.exists(static_dir)})")
print(f"[APP INIT] Templates dir: {templates_dir} (exists: {os.path.exists(templates_dir)})")

# 정적 파일 마운트 (Netlify Functions 환경 고려)
static_mounted = False
possible_static_dirs = [
    os.path.join(current_dir, "..", "..", "netlify", "functions", "static"),  # netlify/functions/static (빌드 시 복사됨)
    os.path.join(project_root, "netlify", "functions", "static"),  # netlify/functions/static
    static_dir,  # 프로젝트 루트/static
    "/var/task/static",  # Netlify Functions 기본 경로
    "/var/task/netlify/functions/static",  # Netlify Functions 패키징 경로
]

for sd in possible_static_dirs:
    if sd and os.path.exists(sd):
        try:
            app.mount("/static", StaticFiles(directory=sd), name="static")
            print(f"[APP INIT] Static files mounted from: {sd}")
            static_mounted = True
            static_dir = sd  # 실제 마운트된 경로 저장
            break
        except Exception as e:
            print(f"[APP INIT] Error mounting static files from {sd}: {e}")
            continue

if not static_mounted:
    print(f"[APP INIT] Warning: Could not mount static files from any location")

# 템플릿 디렉토리 설정 (Netlify Functions 환경 고려)
# Netlify Functions에서는 netlify/functions/templates에 복사됨
templates = None
possible_template_dirs = [
    os.path.join(current_dir, "..", "..", "netlify", "functions", "templates"),  # netlify/functions/templates (빌드 시 복사됨)
    os.path.join(project_root, "netlify", "functions", "templates"),  # netlify/functions/templates
    templates_dir,  # 프로젝트 루트/templates
    os.path.join(current_dir, "..", "templates"),  # app/../templates
    os.path.join(project_root, "templates"),  # 재확인
    "templates",  # 상대 경로
    "/var/task/templates",  # Netlify Functions 기본 경로
    "/var/task/netlify/functions/templates",  # Netlify Functions 패키징 경로
    "/opt/python/templates",  # Lambda 기본 경로
    os.path.join(os.getcwd(), "templates"),  # 현재 작업 디렉토리
]

for template_path in possible_template_dirs:
    abs_path = os.path.abspath(template_path) if template_path and not os.path.isabs(template_path) else template_path
    if abs_path and os.path.exists(abs_path):
        try:
            templates = Jinja2Templates(directory=abs_path)
            print(f"[APP INIT] Templates loaded from: {abs_path}")
            break
        except Exception as e:
            print(f"[APP INIT] Error loading templates from {abs_path}: {e}")
            continue

if templates is None:
    # 최종 fallback: 현재 디렉토리 기준
    try:
        cwd = os.getcwd()
        print(f"[APP INIT] Attempting fallback with cwd: {cwd}")
        templates = Jinja2Templates(directory="templates")
        print("[APP INIT] Templates loaded from default: templates (fallback)")
    except Exception as e:
        print(f"[APP INIT] CRITICAL: Failed to load templates: {e}")
        # 빈 템플릿 객체로 초기화하여 앱이 시작되도록 함
        # 하지만 실제로는 에러 페이지를 반환하도록 함
        pass


def render_error_page(message: str, details: str = "") -> HTMLResponse:
    """에러 페이지 렌더링"""
    error_html = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>오류 - Market Analytics</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-50">
        <div class="max-w-4xl mx-auto px-4 py-16">
            <div class="bg-white rounded-lg shadow-lg p-8">
                <h1 class="text-3xl font-bold text-red-600 mb-4">⚠️ 오류 발생</h1>
                <p class="text-gray-700 text-lg mb-4">{message}</p>
                {f'<pre class="bg-gray-100 p-4 rounded text-sm overflow-auto"><code>{details}</code></pre>' if details else ''}
                <div class="mt-6 space-y-2">
                    <a href="/health" class="text-blue-600 hover:underline block">Health Check 확인</a>
                    <a href="/api/apps/" class="text-blue-600 hover:underline block">API 테스트</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=error_html, status_code=500)


def render_simple_dashboard() -> HTMLResponse:
    """템플릿 없이 간단한 대시보드 렌더링"""
    html_content = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Market Analytics</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-50">
        <nav class="bg-white border-b border-gray-200">
            <div class="max-w-7xl mx-auto px-6 py-4">
                <h1 class="text-2xl font-bold">📊 Market Analytics</h1>
            </div>
        </nav>
        <main class="max-w-7xl mx-auto px-6 py-8">
            <div class="bg-white rounded-lg shadow p-6 mb-6">
                <h2 class="text-xl font-semibold mb-4">서비스 준비 중</h2>
                <p class="text-gray-600 mb-4">템플릿 파일을 찾을 수 없습니다. Functions 로그를 확인해주세요.</p>
                <div class="space-y-2">
                    <a href="/health" class="text-blue-600 hover:underline block">Health Check</a>
                    <a href="/api/apps/" class="text-blue-600 hover:underline block">API 엔드포인트</a>
                </div>
            </div>
        </main>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """메인 대시보드"""
    try:
        if templates is None:
            print("[ROOT] Templates not loaded, rendering simple dashboard")
            return render_simple_dashboard()
        
        return templates.TemplateResponse("dashboard.html", {"request": request})
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"[ERROR] Dashboard render error: {e}")
        print(f"[ERROR] Traceback: {error_details}")
        return render_error_page(f"대시보드 렌더링 오류: {str(e)}", error_details)


@app.get("/apps", response_class=HTMLResponse)
async def apps_page(request: Request):
    """앱 목록 페이지"""
    try:
        if templates is None:
            return render_simple_dashboard()
        return templates.TemplateResponse("apps.html", {"request": request})
    except Exception as e:
        import traceback
        print(f"[ERROR] Apps page render error: {e}")
        return render_error_page(f"앱 페이지 렌더링 오류: {str(e)}", traceback.format_exc())


@app.get("/analysis", response_class=HTMLResponse)
async def analysis_page(request: Request):
    """분석 페이지"""
    try:
        if templates is None:
            return render_simple_dashboard()
        return templates.TemplateResponse("analysis.html", {"request": request})
    except Exception as e:
        import traceback
        print(f"[ERROR] Analysis page render error: {e}")
        return render_error_page(f"분석 페이지 렌더링 오류: {str(e)}", traceback.format_exc())


@app.get("/report", response_class=HTMLResponse)
async def report_page(request: Request):
    """AI 리포트 페이지"""
    try:
        if templates is None:
            return render_simple_dashboard()
        return templates.TemplateResponse("report.html", {"request": request})
    except Exception as e:
        import traceback
        print(f"[ERROR] Report page render error: {e}")
        return render_error_page(f"리포트 페이지 렌더링 오류: {str(e)}", traceback.format_exc())


@app.get("/health")
def health_check():
    """헬스 체크 - 상세 정보 포함"""
    import os
    possible_paths = {
        "project_root": project_root,
        "static_dir": static_dir,
        "templates_dir": templates_dir,
        "current_dir": current_dir,
        "current_file": current_file,
        "cwd": os.getcwd(),
        "LAMBDA_TASK_ROOT": os.environ.get('LAMBDA_TASK_ROOT', 'Not set'),
        "_HANDLER": os.environ.get('_HANDLER', 'Not set'),
    }
    
    path_status = {}
    for name, path in possible_paths.items():
        if path and path != 'Not set':
            try:
                path_status[name] = {
                    "path": path,
                    "exists": os.path.exists(path) if isinstance(path, str) else False
                }
            except:
                path_status[name] = {"path": path, "exists": False, "error": "Cannot check"}
        else:
            path_status[name] = {"path": path, "exists": False}
    
    # 템플릿 디렉토리 확인
    template_dirs_to_check = [
        templates_dir,
        os.path.join(current_dir, "..", "templates"),
        os.path.join(project_root, "templates"),
        "templates",
        "/var/task/templates",
        "/opt/python/templates",
        os.path.join(os.getcwd(), "templates")
    ]
    
    template_status = []
    for td in template_dirs_to_check:
        if td:
            try:
                abs_td = os.path.abspath(td) if not os.path.isabs(td) else td
                exists = os.path.exists(abs_td) if abs_td else False
                template_status.append({
                    "path": abs_td,
                    "exists": exists
                })
            except Exception as e:
                template_status.append({
                    "path": td,
                    "exists": False,
                    "error": str(e)
                })
    
    # 파일 목록 확인
    file_list = {}
    if templates_dir:
        try:
            if os.path.exists(templates_dir):
                file_list["templates"] = os.listdir(templates_dir)
            else:
                file_list["templates"] = "Directory does not exist"
        except Exception as e:
            file_list["templates"] = f"Cannot read: {str(e)}"
    
    if static_dir:
        try:
            if os.path.exists(static_dir):
                file_list["static"] = os.listdir(static_dir)
            else:
                file_list["static"] = "Directory does not exist"
        except Exception as e:
            file_list["static"] = f"Cannot read: {str(e)}"
    
    # 현재 디렉토리 전체 구조 확인 (최상위 20개만)
    try:
        cwd_contents = []
        if os.path.exists(os.getcwd()):
            items = list(os.listdir(os.getcwd()))[:20]
            for item in items:
                item_path = os.path.join(os.getcwd(), item)
                cwd_contents.append({
                    "name": item,
                    "is_dir": os.path.isdir(item_path),
                    "exists": True
                })
        file_list["cwd_contents"] = cwd_contents
    except Exception as e:
        file_list["cwd_contents"] = f"Error: {str(e)}"
    
    return {
        "status": "ok" if templates is not None else "error",
        "templates_loaded": templates is not None,
        "static_mounted": static_mounted,
        "paths": path_status,
        "template_dirs_checked": template_status,
        "files": file_list,
        "sys_path_first_5": sys.path[:5] if 'sys' in dir() else []
    }


@app.get("/test")
def test_endpoint():
    """간단한 테스트 엔드포인트"""
    return {"message": "서버가 정상적으로 작동 중입니다", "timestamp": "2024-01-10"}
