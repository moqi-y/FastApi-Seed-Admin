from sqlmodel import Session, select

from app.crud.database import engine
from app.models.user_role import UserRole
from app.schemas.user_role import UserRoleCreate, UserRoleUpdate


async def get_user_roles(user_id: int):
    with Session(engine) as session:
        return session.exec(select(UserRole).where(UserRole.user_id == user_id)).all()


async def get_user_role_ids(user_id: int):
    """Return role IDs for the user-edit form."""
    with Session(engine) as session:
        return session.exec(
            select(UserRole.role_id).where(UserRole.user_id == user_id)
        ).all()


async def add_user_role(data: UserRoleCreate):
    with Session(engine) as session:
        existing = session.exec(
            select(UserRole).where(
                UserRole.user_id == data.user_id, UserRole.role_id == data.role_id
            )
        ).first()
        if existing:
            return None
        relation = UserRole(user_id=data.user_id, role_id=data.role_id)
        session.add(relation)
        session.commit()
        session.refresh(relation)
        return relation


async def get_user_role_by_id(user_role_id: int):
    with Session(engine) as session:
        return session.get(UserRole, user_role_id)


async def update_user_role(data: UserRoleUpdate):
    with Session(engine) as session:
        relation = session.exec(
            select(UserRole).where(
                UserRole.user_id == data.user_id, UserRole.role_id == data.role_id
            )
        ).first()
        if relation:
            return True
        session.add(UserRole(user_id=data.user_id, role_id=data.role_id))
        session.commit()
        return True


async def delete_user_role(user_role_id: int):
    with Session(engine) as session:
        relation = session.get(UserRole, user_role_id)
        if not relation:
            return False
        session.delete(relation)
        session.commit()
        return True
