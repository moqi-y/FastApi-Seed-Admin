from datetime import datetime

from sqlalchemy import func
from sqlmodel import Session, select

from app.crud.database import engine
from app.models.role import Role
from app.models.user_role import UserRole
from app.schemas.role import RoleCreate, RoleUpdate


async def get_roles_list(page_num: int, page_size: int, keywords: str | None = None):
    with Session(engine) as session:
        statement = select(Role)
        count_statement = select(func.count()).select_from(Role)
        if keywords:
            condition = Role.name.contains(keywords)
            statement = statement.where(condition)
            count_statement = count_statement.where(condition)
        total = session.exec(count_statement).one()
        roles = session.exec(
            statement.order_by(Role.roleId).offset((page_num - 1) * page_size).limit(page_size)
        ).all()
        return {"total": total, "list": roles}


async def get_role_by_name(name: str):
    with Session(engine) as session:
        return session.exec(select(Role).where(Role.name == name)).first()


async def get_roles_options():
    with Session(engine) as session:
        return session.exec(select(Role).where(Role.status == 1).order_by(Role.roleId)).all()


async def get_user_roles_codes(user_id: int):
    with Session(engine) as session:
        statement = (
            select(Role.code)
            .join(UserRole, Role.roleId == UserRole.role_id)
            .where(UserRole.user_id == user_id, Role.status == 1)
        )
        return session.exec(statement).all()


async def get_role_by_id(role_id: int):
    with Session(engine) as session:
        return session.get(Role, role_id)


async def get_role_by_code(role_code: str):
    with Session(engine) as session:
        return session.exec(select(Role).where(Role.code == role_code)).first()


async def add_role(data: RoleCreate):
    with Session(engine) as session:
        exists = session.exec(
            select(Role).where((Role.name == data.name) | (Role.code == data.code))
        ).first()
        if exists:
            return None
        role = Role(
            name=data.name,
            code=data.code,
            status=data.status if data.status is not None else 1,
            description=data.description,
        )
        session.add(role)
        session.commit()
        session.refresh(role)
        return role


async def update_role(data: RoleUpdate, role_id: int):
    with Session(engine) as session:
        role = session.get(Role, role_id)
        if not role:
            return None
        duplicate = session.exec(
            select(Role).where(Role.code == data.code, Role.roleId != role_id)
        ).first()
        if duplicate:
            return None
        role.name = data.name
        role.code = data.code
        role.status = data.status if data.status is not None else role.status
        role.description = data.description
        role.updateTime = datetime.now()
        session.add(role)
        session.commit()
        session.refresh(role)
        return role


async def delete_roles(role_ids: list[int]):
    with Session(engine) as session:
        protected = session.exec(
            select(Role).where(Role.roleId.in_(role_ids), Role.code == "admin")
        ).first()
        if protected:
            return False
        for role in session.exec(select(Role).where(Role.roleId.in_(role_ids))).all():
            session.delete(role)
        session.commit()
        return True
