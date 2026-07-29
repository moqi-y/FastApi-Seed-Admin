from datetime import datetime

from sqlmodel import Session, delete, select

from app.crud.database import engine
from app.models.role_permission import RolePermission


async def list_role_permissions(role_id: int):
    with Session(engine) as session:
        return session.exec(
            select(RolePermission).where(RolePermission.role_id == role_id)
        ).all()


async def get_role_menu_ids(role_id: int):
    with Session(engine) as session:
        return session.exec(
            select(RolePermission.permission_id).where(RolePermission.role_id == role_id)
        ).all()


async def add_role_permission(role_id: int, permission_id: int):
    with Session(engine) as session:
        existing = session.exec(
            select(RolePermission).where(
                RolePermission.role_id == role_id,
                RolePermission.permission_id == permission_id,
            )
        ).first()
        if existing:
            return None
        relation = RolePermission(role_id=role_id, permission_id=permission_id)
        session.add(relation)
        session.commit()
        session.refresh(relation)
        return relation


async def update_role_permission(role_id: int, permission_ids: list[int]):
    with Session(engine) as session:
        session.exec(delete(RolePermission).where(RolePermission.role_id == role_id))
        now = datetime.now()
        session.add_all(
            [
                RolePermission(
                    role_id=role_id,
                    permission_id=permission_id,
                    created_at=now,
                    updated_at=now,
                )
                for permission_id in set(permission_ids)
            ]
        )
        session.commit()
        return True


async def delete_role_permissions(relation_id: int):
    with Session(engine) as session:
        relation = session.get(RolePermission, relation_id)
        if not relation:
            return False
        session.delete(relation)
        session.commit()
        return True
