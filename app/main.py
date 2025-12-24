import os

from fastapi import FastAPI, applications
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from app.crud.database import create_db_and_tables
from app.middleware import cors
from app.middleware.logger_config import make_logging_middleware
from app.routers import router_config

# 加载 .env 文件
load_dotenv()


# 在线API接口文档
def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args, **kwargs,
        # swagger_js_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.20.0/swagger-ui-bundle.min.js",
        # swagger_css_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.20.0/swagger-ui.min.css",
        swagger_js_url="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.20.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.20.0/swagger-ui.min.css",
    )


applications.get_swagger_ui_html = swagger_monkey_patch
debug = os.getenv("APP_DEBUG", "").lower() in ("1", "true")
app = FastAPI(
    title=os.getenv("APP_NAME"),
    description=os.getenv("APP_NAME") + " swagger接口文档",
    version=os.getenv("APP_VERSION"),
    docs_url="/docs" if debug else None,  # docs_url=None, redoc_url=None
    redoc_url="/redoc" if debug else None,
)


@app.on_event("startup")
def on_startup():
    # 创建数据库和表
    create_db_and_tables()


#  跨域设置
cors.cors_config(app)

# 路由配置
router_config(app)

# 注册日志中间件
app.middleware("http")(make_logging_middleware())

#  静态文件配置
app.mount("/static", StaticFiles(directory="static"), name="static")
