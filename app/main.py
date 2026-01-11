"""
Application Market Analytics - FastAPI Application
Railway 배포용
"""
import os
import sys
import asyncio
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates

# 환경 변수 로드 (로컬 개발용)
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

# 초기 로그
print(f"[INIT] Python version: {sys.version}")
print(f"[INIT] Working directory: {os.getcwd()}")
print(f"[INIT] PORT environment variable: {os.getenv('PORT', 'NOT SET')}")

try:
    from app.database import engine, Base
    from app.routers import apps, analysis, upload, report, playstore
    print("[INIT] ✅ All modules imported successfully")
except Exception as e:
    print(f"[INIT] ❌ ERROR importing modules: {e}")
    import traceback
    traceback.print_exc()
    raise

# 데이터베이스 테이블 생성
try:
    Base.metadata.create_all(bind=engine)
    print(f"[APP INIT] ✅ Database tables created successfully")
except Exception as e:
    # 읽기 전용 파일 시스템 등에서 실패할 수 있음
    print(f"[APP INIT] ⚠️ Warning: Database initialization failed: {e}")
    print(f"[APP INIT] Continuing without database initialization...")

app = FastAPI(title="Application Market Analytics", version="1.0.0")

# 전역 예외 핸들러 추가
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """전역 예외 핸들러 - 모든 예외를 잡아서 로깅하고 적절한 응답 반환"""
    import logging
    import traceback
    logger = logging.getLogger(__name__)
    
    # 상세한 에러 로깅
    error_detail = traceback.format_exc()
    logger.error(f"Unhandled exception: {exc}")
    logger.error(f"Request URL: {request.url}")
    logger.error(f"Request method: {request.method}")
    logger.error(f"Traceback: {error_detail}")
    
    # HTTPException은 그대로 전달
    from fastapi import HTTPException
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )
    
    # 기타 예외는 500 에러로 반환
    return JSONResponse(
        status_code=500,
        content={
            "detail": f"서버 내부 오류가 발생했습니다: {str(exc)}",
            "error_type": type(exc).__name__
        }
    )

# Favicon 엔드포인트 (404 방지)
@app.get("/favicon.ico")
async def favicon():
    """Favicon 요청 처리 (404 방지)"""
    from fastapi.responses import Response
    return Response(status_code=204)  # No Content

# 헬스 체크 엔드포인트
@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    health_status = {
        "status": "healthy",
        "database": "unknown",
        "openai": "unknown"
    }
    
    # 데이터베이스 체크
    try:
        from app.database import SessionLocal
        from sqlalchemy import text
        db = SessionLocal()
        try:
            db.execute(text("SELECT 1"))
            db.commit()
            health_status["database"] = "connected"
        finally:
            db.close()
    except Exception as e:
        health_status["database"] = "disconnected"
        health_status["status"] = "unhealthy"
        health_status["database_error"] = str(e)
    
    # OpenAI API 키 체크
    try:
        from app.config import settings
        if settings.OPENAI_API_KEY:
            # API 키가 설정되어 있는지만 확인 (실제 API 호출은 하지 않음)
            api_key_prefix = settings.OPENAI_API_KEY[:10] if len(settings.OPENAI_API_KEY) > 10 else "***"
            health_status["openai"] = f"configured (prefix: {api_key_prefix}...)"
        else:
            health_status["openai"] = "not_configured"
    except Exception as e:
        health_status["openai"] = "error"
        health_status["openai_error"] = str(e)
    
    return health_status

# 라우터 등록 (에러가 발생해도 앱이 시작되도록)
try:
    app.include_router(apps.router)
    app.include_router(analysis.router)
    app.include_router(upload.router)
    app.include_router(report.router)
    app.include_router(playstore.router)
    print(f"[APP INIT] ✅ All routers registered successfully")
except Exception as e:
    print(f"[APP INIT] ⚠️ Warning: Router registration failed: {e}")
    import traceback
    traceback.print_exc()

# 정적 파일 및 템플릿 경로
# 프로젝트 루트 찾기
current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)

# 프로젝트 루트 찾기 (Railway 환경 고려)
if current_dir.endswith("app"):
    project_root = os.path.dirname(current_dir)
else:
    project_root = os.path.dirname(current_dir)

# Railway 환경에서는 현재 작업 디렉토리가 프로젝트 루트
# Lambda/Netlify Functions 환경에서의 경로 확인
LAMBDA_TASK_ROOT = os.environ.get('LAMBDA_TASK_ROOT', '')
if LAMBDA_TASK_ROOT:
    project_root = LAMBDA_TASK_ROOT
elif os.path.exists(os.path.join(os.getcwd(), "app")) and os.path.exists(os.path.join(os.getcwd(), "templates")):
    # Railway 등에서 cwd가 프로젝트 루트인 경우
    project_root = os.getcwd()

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
# 현재 파일 기준으로 상위 디렉토리에서 static 찾기
static_mounted = False
possible_static_dirs = [
    os.path.join(current_dir, "..", "static"),  # app/../static (로컬) 또는 netlify/functions/static (Functions)
    os.path.join(current_dir, "..", "..", "static"),  # app/../../static (프로젝트 루트)
    os.path.join(project_root, "static"),  # 프로젝트 루트/static
    static_dir,  # 프로젝트 루트/static (재확인)
    "/var/task/static",  # Netlify Functions 기본 경로 (/var/task = Functions 루트)
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
# Netlify Functions에서는 server.py와 같은 디렉토리에 templates/가 있음 (빌드 시 복사됨)
# server.py 위치: netlify/functions/server.py
# app/main.py 위치: netlify/functions/app/main.py (빌드 시 복사됨)
# templates 위치: netlify/functions/templates/ (빌드 시 복사됨)
templates = None

# 현재 파일 기준으로 상위 디렉토리에서 templates 찾기
# app/main.py -> netlify/functions/app/main.py -> netlify/functions/templates/
possible_template_dirs = [
    os.path.join(current_dir, "..", "templates"),  # app/../templates (로컬) 또는 netlify/functions/templates (Functions)
    os.path.join(current_dir, "..", "..", "templates"),  # app/../../templates (프로젝트 루트)
    os.path.join(project_root, "templates"),  # 프로젝트 루트/templates
    templates_dir,  # 프로젝트 루트/templates (재확인)
    "templates",  # 상대 경로
    "/var/task/templates",  # Netlify Functions 기본 경로 (/var/task = Functions 루트)
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


@app.get("/category-analysis", response_class=HTMLResponse)
async def category_analysis_page(request: Request):
    """카테고리별 분석 페이지"""
    try:
        if templates is None:
            return render_simple_dashboard()
        return templates.TemplateResponse("category_analysis.html", {"request": request})
    except Exception as e:
        import traceback
        print(f"[ERROR] Category analysis page render error: {e}")
        return render_error_page(f"카테고리 분석 페이지 렌더링 오류: {str(e)}", traceback.format_exc())


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

# 앱 시작 완료 로그 (모듈 로드 시 실행)
def print_startup_info():
    """앱 시작 정보 출력"""
    import sys
    sys.stdout.flush()
    print("=" * 60)
    print("🚀 Application Market Analytics Initialized!")
    print(f"   FastAPI: {app.title} v{app.version}")
    print(f"   Routes: {len(app.routes)}")
    print(f"   Static files mounted: {static_mounted}")
    print(f"   Templates loaded: {templates is not None}")
    print(f"   PORT: {os.getenv('PORT', 'NOT SET')}")
    print("=" * 60)
    sys.stdout.flush()

# 모듈 로드 시 실행
print_startup_info()

# FastAPI startup event
@app.on_event("startup")
async def startup_event():
    """앱 시작 시 실행"""
    import sys
    sys.stdout.flush()
    print("✅ FastAPI application started successfully!")
    print(f"   Listening on 0.0.0.0:{os.getenv('PORT', '8000')}")
    
    # 월요일이면 Play Store 순위 자동 가져오기
    try:
        from app.services.play_store_scraper import should_fetch_this_week
        from app.tasks.scheduler import check_and_fetch_rankings
        if should_fetch_this_week():
            print("📅 월요일 감지: Play Store 순위 자동 가져오기 시작...")
            # 백그라운드에서 실행 (앱 시작을 블로킹하지 않음)
            asyncio.create_task(check_and_fetch_rankings())
    except Exception as e:
        print(f"⚠️ Play Store 스케줄러 시작 실패: {e}")
    
    sys.stdout.flush()

# 앱 시작 시 로그 출력
if __name__ != "__main__":
    print("=" * 50)
    print("🚀 Application Market Analytics Starting...")
    print(f"✅ FastAPI app created: {app.title}")
    print(f"✅ Routes registered: {len(app.routes)}")
    print(f"✅ Static files: {static_mounted}")
    print(f"✅ Templates: {templates is not None}")
    print("=" * 50)
