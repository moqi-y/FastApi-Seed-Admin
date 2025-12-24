from fastapi import Depends

from app.dependencies import get_current_user
from app.routers import auth, users, files, roles, permissions, user_role, role_perms, menu


def router_config(app):
    # 将auth.router添加到app中，路径名为/api/v1/auth，文档标签名为auth
    app.include_router(
        auth.router,
        prefix="/api/v1/auth",  # 路径名
        tags=["auth"]  # 文档标签名
        # dependencies=[Depends(get_current_user)] #依赖
    )

    app.include_router(
        users.router,
        deprecated=False,  # 是否弃用
        prefix="/api/v1/users",  # 路径名
        tags=["user"]  # 文档标签名
        # dependencies=[Depends(get_current_user)] #依赖
    )

    app.include_router(
        files.router,
        prefix="/api/v1/files",  # 路径名
        tags=["files"],  # 文档标签名
        dependencies=[Depends(get_current_user)]
    )

    app.include_router(
        roles.router,
        prefix="/api/v1/roles",  # 路径名
        tags=["roles"]  # 文档标签名
    )

    app.include_router(
        permissions.router,
        prefix="/api/v1/perm",  # 路径名
        tags=["permissions"]  # 文档标签名
    )

    app.include_router(
        user_role.router,
        prefix="/api/v1/user_roles",  # 路径名
        tags=["user_roles"]  # 文档标签名
    )

    app.include_router(
        role_perms.router,
        prefix="/api/v1/role_perms",  # 路径名
        tags=["role_perms"]  # 文档标签名
    )

    app.include_router(
        menu.router,
        prefix="/api/v1/menus",  # 路径名
        tags=["menus"],  # 文档标签名
        dependencies=[Depends(get_current_user)]
    )
