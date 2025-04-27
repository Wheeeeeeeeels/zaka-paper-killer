from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from api.routes import paper, auth
from core.config import settings
import os

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建templates目录
os.makedirs("templates", exist_ok=True)

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

# 配置模板
templates = Jinja2Templates(directory="templates")

# 包含路由
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(paper.router, prefix=f"{settings.API_V1_STR}/papers", tags=["papers"])

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "project_name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "api_docs_url": "/docs",
        "redoc_url": "/redoc",
        "api_base_url": settings.API_V1_STR,
        "features": [
            {
                "name": "论文管理",
                "description": "上传、存储和管理学术论文",
                "endpoints": [
                    {"path": "/papers", "method": "GET", "description": "获取论文列表"},
                    {"path": "/papers/upload", "method": "POST", "description": "上传新论文"},
                    {"path": "/papers/{paper_id}", "method": "GET", "description": "获取论文详情"}
                ]
            },
            {
                "name": "论文分析",
                "description": "自动分析论文内容，提取关键信息",
                "endpoints": [
                    {"path": "/papers/{paper_id}/analysis", "method": "POST", "description": "创建论文分析"},
                    {"path": "/papers/{paper_id}/analysis", "method": "GET", "description": "获取分析结果"}
                ]
            },
            {
                "name": "用户认证",
                "description": "安全的用户认证和授权系统",
                "endpoints": [
                    {"path": "/auth/register", "method": "POST", "description": "用户注册"},
                    {"path": "/auth/token", "method": "POST", "description": "用户登录"}
                ]
            }
        ]
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 