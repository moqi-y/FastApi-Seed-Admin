import os
import time
import logging
from logging.handlers import RotatingFileHandler
from fastapi import Request

# -----------------------------
# 1. 日志目录 & 格式
# -----------------------------
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# -----------------------------
# 2. 全局 logger（供业务代码直接 import）
# -----------------------------
logger = logging.getLogger("fastapi_app")
logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler(
    os.path.join(LOG_DIR, "app.log"),
    maxBytes=10 * 1024 * 1024,  # 10 MB
    backupCount=5,
    encoding="utf-8"
)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(file_handler)


# -----------------------------
# 3. 中间件工厂（供 main.py 调用）
# -----------------------------
def make_logging_middleware():
    """返回一个可被 @app.middleware('http') 使用的异步中间件函数"""

    async def logging_middleware(request: Request, call_next):
        start = time.time()
        logger.info(f"→ {request.method} {request.url.path} - Client: {request.client.host}")

        response = await call_next(request)
        duration = round((time.time() - start) * 1000, 2)
        logger.info(
            f"← {request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Duration: {duration}ms"
        )
        return response

    return logging_middleware


# 主动记录日志
async def log_info(message: str):
    logger.info(f"{message}")
