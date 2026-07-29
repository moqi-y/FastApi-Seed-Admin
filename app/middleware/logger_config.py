import logging
import os
import time
from logging.handlers import RotatingFileHandler

from fastapi import Request

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

logger = logging.getLogger("fastapi_app")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = RotatingFileHandler(
        os.path.join(LOG_DIR, "app.log"),
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(handler)


def make_logging_middleware():
    async def logging_middleware(request: Request, call_next):
        start = time.perf_counter()
        client_host = request.client.host if request.client else "unknown"
        logger.info("%s %s - Client: %s", request.method, request.url.path, client_host)
        response = await call_next(request)
        duration = round((time.perf_counter() - start) * 1000, 2)
        logger.info(
            "%s %s - Status: %s - Duration: %sms",
            request.method, request.url.path, response.status_code, duration,
        )
        return response

    return logging_middleware


async def log_info(message: str):
    logger.info("%s", message)
