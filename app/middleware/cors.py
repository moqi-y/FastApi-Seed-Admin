from fastapi.middleware.cors import CORSMiddleware


# 定义一个函数，用于配置跨域资源共享（CORS）
def cors_config(app):
    # 定义允许的源
    origins = [
        "*"
    ]
    # 添加中间件，用于处理跨域请求
    app.add_middleware(
        CORSMiddleware,
        # 允许的源
        allow_origins=origins,
        # 是否允许携带凭证
        allow_credentials=True,
        # 允许的方法
        allow_methods=["*"],
        # 允许的头部
        allow_headers=["*"],
    )
