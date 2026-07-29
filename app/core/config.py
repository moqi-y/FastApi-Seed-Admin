"""Centralized application configuration."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _as_list(value: str | None, default: list[str]) -> list[str]:
    if not value:
        return default
    return [item.strip() for item in value.split(",") if item.strip()]


class Settings:
    app_name = os.getenv("APP_NAME", "FastAPI Admin")
    app_version = os.getenv("APP_VERSION", "1.0.0")
    app_description = os.getenv("APP_DESCRIPTION", "Reusable FastAPI admin backend")
    app_host = os.getenv("APP_HOST", "127.0.0.1")
    app_port = int(os.getenv("APP_PORT", "8080"))
    debug = _as_bool(os.getenv("APP_DEBUG"))
    api_prefix = os.getenv("API_PREFIX", "/api/v1").rstrip("/")

    sql_type = os.getenv("SQL_TYPE", "sqlite").lower()
    sqlite_file = os.getenv("SQLITE_FILE", str(ROOT_DIR / "FastApi-Seed-Admin.db"))
    mysql_host = os.getenv("MYSQL_HOST", "127.0.0.1")
    mysql_port = int(os.getenv("MYSQL_PORT", "3306"))
    mysql_user = os.getenv("MYSQL_USER", "root")
    mysql_password = os.getenv("MYSQL_PASSWORD", "")
    mysql_db = os.getenv("MYSQL_DB", "fastapi_admin")

    jwt_secret_key = os.getenv("JWT_SECRET_KEY", "change-me-in-production")
    jwt_expire_minutes = int(os.getenv("JWT_EXPIRE_MINUTES", "30"))
    use_captcha = _as_bool(os.getenv("USE_CAPTCHA"))
    cors_origins = _as_list(
        os.getenv("CORS_ORIGINS"), ["http://localhost:3000", "http://127.0.0.1:3000"]
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
