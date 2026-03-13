import os

import uvicorn

from app import main

# 启动主程序
if __name__ == '__main__':
    uvicorn.run(
        app=main.app,
        host=os.getenv("APP_HOST"),
        port=int(os.getenv("APP_PORT")))
