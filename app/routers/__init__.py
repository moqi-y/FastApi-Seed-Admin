from fastapi import Depends

from app.core.config import get_settings
from app.dependencies import get_current_user, require_admin
from app.routers import (
    auth,
    dicts,
    files,
    health,
    menu,
    permissions,
    role_perms,
    roles,
    user_role,
    users,
)


def router_config(app):
    """Register built-in modules using one configurable API prefix."""
    prefix = get_settings().api_prefix
    app.include_router(health.router, prefix=prefix)
    app.include_router(auth.router, prefix=f"{prefix}/auth", tags=["auth"])
    app.include_router(users.router, prefix=f"{prefix}/users", tags=["user"])
    app.include_router(
        files.router,
        prefix=f"{prefix}/files",
        tags=["files"],
        dependencies=[Depends(get_current_user)],
    )
    app.include_router(
        roles.router,
        prefix=f"{prefix}/roles",
        tags=["roles"],
        dependencies=[Depends(require_admin)],
    )
    app.include_router(
        permissions.router,
        prefix=f"{prefix}/perm",
        tags=["permissions"],
        dependencies=[Depends(require_admin)],
    )
    app.include_router(
        user_role.router,
        prefix=f"{prefix}/user_roles",
        tags=["user_roles"],
        dependencies=[Depends(require_admin)],
    )
    app.include_router(
        role_perms.router,
        prefix=f"{prefix}/role_perms",
        tags=["role_perms"],
        dependencies=[Depends(require_admin)],
    )
    app.include_router(
        menu.router,
        prefix=f"{prefix}/menus",
        tags=["menus"],
        dependencies=[Depends(get_current_user)],
    )
    app.include_router(
        dicts.router,
        prefix=f"{prefix}/dicts",
        tags=["dicts"],
        dependencies=[Depends(get_current_user)],
    )
