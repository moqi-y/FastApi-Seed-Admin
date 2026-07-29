from datetime import datetime

from sqlalchemy import func
from sqlmodel import Session, select

from app.crud.database import engine
from app.models.permission import Perm
from app.models.role_permission import RolePermission
from app.models.user_role import UserRole
from app.schemas.perm import PermCreate, PermUpdate


async def get_perms_list(page_num: int, page_size: int, keyword: str | None = None):
    with Session(engine) as session:
        statement = select(Perm)
        count_statement = select(func.count()).select_from(Perm)
        if keyword:
            condition = Perm.name.contains(keyword)
            statement = statement.where(condition)
            count_statement = count_statement.where(condition)
        total = session.exec(count_statement).one()
        rows = session.exec(
            statement.order_by(Perm.sort, Perm.permission_id)
            .offset((page_num - 1) * page_size)
            .limit(page_size)
        ).all()
        return {"total": total, "list": rows}


async def get_perm_options():
    with Session(engine) as session:
        permissions = session.exec(select(Perm).order_by(Perm.sort, Perm.permission_id)).all()
    nodes = {
        permission.permission_id: {
            "parentId": permission.parent_id,
            "label": permission.name,
            "value": permission.permission_id,
            "id": permission.permission_id,
            "path": permission.path,
            "type": permission.type,
            "icon": permission.icon or "",
            "name": permission.name,
            "children": [],
        }
        for permission in permissions
    }
    roots = []
    for node in nodes.values():
        parent = nodes.get(node["parentId"])
        if parent:
            parent["children"].append(node)
        else:
            roots.append(node)
    return roots


async def get_perm_by_id(permission_id: int):
    with Session(engine) as session:
        return session.get(Perm, permission_id)


async def get_user_perm_codes(user_id: int):
    with Session(engine) as session:
        statement = (
            select(Perm.code)
            .distinct()
            .join(RolePermission, Perm.permission_id == RolePermission.permission_id)
            .join(UserRole, RolePermission.role_id == UserRole.role_id)
            .where(UserRole.user_id == user_id, Perm.status != 0)
        )
        return session.exec(statement).all()


async def add_perm(data: PermCreate):
    with Session(engine) as session:
        if session.exec(select(Perm).where(Perm.code == data.code)).first():
            return None
        permission = Perm(**data.model_dump())
        session.add(permission)
        session.commit()
        session.refresh(permission)
        return permission


async def update_perm(data: PermUpdate):
    with Session(engine) as session:
        permission = session.get(Perm, data.permission_id)
        if not permission:
            return None
        duplicate = session.exec(
            select(Perm).where(Perm.code == data.code, Perm.permission_id != data.permission_id)
        ).first()
        if duplicate:
            return None
        for field, value in data.model_dump(exclude={"permission_id"}).items():
            setattr(permission, field, value)
        permission.update_time = datetime.now()
        session.add(permission)
        session.commit()
        session.refresh(permission)
        return permission


async def delete_perm(permission_id: int):
    with Session(engine) as session:
        permission = session.get(Perm, permission_id)
        if not permission:
            return None
        children = session.exec(select(Perm).where(Perm.parent_id == permission_id)).first()
        if children:
            return None
        session.delete(permission)
        session.commit()
        return permission
