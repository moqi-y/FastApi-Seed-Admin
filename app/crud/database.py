from urllib.parse import quote_plus

from sqlmodel import Session, SQLModel, create_engine

from app.core.config import get_settings

settings = get_settings()

if settings.sql_type == "mysql":
    database_url = (
        f"mysql+pymysql://{settings.mysql_user}:{quote_plus(settings.mysql_password)}"
        f"@{settings.mysql_host}:{settings.mysql_port}/{settings.mysql_db}"
    )
    engine = create_engine(
        database_url, pool_recycle=3600, pool_pre_ping=True, echo=settings.debug
    )
elif settings.sql_type == "sqlite":
    engine = create_engine(
        f"sqlite:///{settings.sqlite_file}",
        echo=settings.debug,
        connect_args={"check_same_thread": False},
    )
else:
    raise ValueError("SQL_TYPE must be either 'mysql' or 'sqlite'")


def create_db_and_tables() -> None:
    """Create the schema and seed the required administration records."""
    # Import every table model before SQLModel collects metadata. This keeps
    # standalone initialization commands consistent with application startup.
    from app.models import captcha, dict, dict_data, menu, permission, role, role_permission, user, user_role

    SQLModel.metadata.create_all(bind=engine)
    seed_initial_data()


def seed_initial_data() -> None:
    from app.core.security import hash_password
    from app.models.permission import Perm
    from app.models.role import Role
    from app.models.role_permission import RolePermission
    from app.models.user import User
    from app.models.user_role import UserRole

    permissions = [
        ("系统管理", "sys", 0, "2", "/system", 1),
        ("用户管理", "sys:user", 1, "1", "/system/user", 10),
        ("查询用户", "sys:user:query", 2, "4", None, 1),
        ("新增用户", "sys:user:add", 2, "4", None, 2),
        ("编辑用户", "sys:user:edit", 2, "4", None, 3),
        ("删除用户", "sys:user:delete", 2, "4", None, 4),
        ("角色管理", "sys:role", 1, "1", "/system/role", 20),
        ("查询角色", "sys:role:query", 7, "4", None, 1),
        ("新增角色", "sys:role:add", 7, "4", None, 2),
        ("编辑角色", "sys:role:edit", 7, "4", None, 3),
        ("删除角色", "sys:role:delete", 7, "4", None, 4),
        ("权限管理", "sys:permission", 1, "1", "/system/permission", 30),
    ]
    with Session(engine) as session:
        admin_role = session.query(Role).filter(Role.code == "admin").first()
        if not admin_role:
            admin_role = Role(name="管理员", code="admin", status=1, description="系统管理员")
            session.add(admin_role)
            session.flush()
        if not session.query(Role).filter(Role.code == "user").first():
            session.add(Role(name="普通用户", code="user", status=1, description="普通后台用户"))

        admin_user = session.query(User).filter(User.username == "admin").first()
        if not admin_user:
            admin_user = User(
                username="admin",
                nickname="系统管理员",
                password=hash_password("123456"),
                status=1,
            )
            session.add(admin_user)
            session.flush()

        if not session.query(UserRole).filter(
            UserRole.user_id == admin_user.id, UserRole.role_id == admin_role.roleId
        ).first():
            session.add(UserRole(user_id=admin_user.id, role_id=admin_role.roleId))

        permission_ids = []
        for name, code, parent_id, type_, path, sort in permissions:
            permission = session.query(Perm).filter(Perm.code == code).first()
            if not permission:
                permission = Perm(
                    name=name,
                    code=code,
                    parent_id=parent_id,
                    type=type_,
                    path=path,
                    sort=sort,
                    status=1,
                )
                session.add(permission)
                session.flush()
            permission_ids.append(permission.permission_id)

        existing_ids = {
            row.permission_id
            for row in session.query(RolePermission).filter(
                RolePermission.role_id == admin_role.roleId
            )
        }
        session.add_all(
            [
                RolePermission(role_id=admin_role.roleId, permission_id=permission_id)
                for permission_id in permission_ids
                if permission_id not in existing_ids
            ]
        )
        session.commit()


def get_session():
    """Yield one short-lived database session per request."""
    with Session(engine) as session:
        yield session
