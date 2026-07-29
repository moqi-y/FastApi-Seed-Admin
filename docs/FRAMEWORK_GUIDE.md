# 后台框架使用指南

## 已提供的基础能力

- JWT 登录、可选图形验证码、统一成功/错误响应。
- 用户、角色、权限和用户-角色、角色-权限关联管理。
- `admin` 角色保护：用户管理、角色管理和权限管理的写操作不会暴露给普通登录用户。
- 可配置 API 前缀、跨域、SQLite/MySQL 数据库和启动健康检查。
- 每次数据库操作使用独立会话，避免请求并发时出现会话关闭或串用。

## 新项目接入

1. 从 `.env.example` 复制出 `.env`，修改应用名、数据库和 JWT 密钥。
2. 将业务模型放在 `app/models`，路由放在 `app/routers`，并在 `app/routers/__init__.py` 中注册。
3. 需要管理员维护的模块，在 `include_router` 中加上 `dependencies=[Depends(require_admin)]`；普通登录用户模块使用 `get_current_user`。
4. 前端请求统一使用 `API_PREFIX`（默认 `/api/v1`）。上线前将 `APP_DEBUG=false`，设置强随机 `JWT_SECRET_KEY` 和精确 `CORS_ORIGINS`。

## 数据库兼容

这是初始化项目，数据库结构以 app/models 为唯一标准。开发环境启动时自动建表并初始化 admin / 123456 管理员账号、基础角色和权限；生产环境请使用版本化 SQL/Alembic 迁移脚本。
