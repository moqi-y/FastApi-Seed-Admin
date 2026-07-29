from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, applications
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles

from app.core.config import ROOT_DIR, get_settings
from app.core.exceptions import http_exception_handler, validation_exception_handler
from app.crud.database import create_db_and_tables
from app.middleware import cors
from app.middleware.logger_config import make_logging_middleware
from app.routers import router_config

settings = get_settings()


def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args,
        **kwargs,
        swagger_js_url="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.20.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.20.0/swagger-ui.min.css",
    )


applications.get_swagger_ui_html = swagger_monkey_patch


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan,
)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

cors.cors_config(app)
router_config(app)
app.middleware("http")(make_logging_middleware())
app.mount("/static", StaticFiles(directory=str(ROOT_DIR / "static")), name="static")
