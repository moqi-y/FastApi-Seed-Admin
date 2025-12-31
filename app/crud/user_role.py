from sqlmodel import Session, select

from app.crud.database import engine
from app.models.user_role import UserRole
from app.schemas.user_role import UserRoleCreate, UserRoleUpdate

session = Session(engine)


async def get_user_roles(user_id: int):
    try:
        query = select(UserRole).where(UserRole.user_id == user_id)
        result = session.exec(query).all()
        if result:
            return result
        return None
    except Exception as e:
        print("SQL Error: ", e)
        return None
    finally:
        session.close()


async def add_user_role(user_role: UserRoleCreate):
    try:
        query = select(UserRole).where(UserRole.user_id == user_role.user_id, UserRole.role_id == user_role.role_id)
        result = session.exec(query).first()
        if result:
            return None
        new_user_role = UserRole(user_id=user_role.user_id, role_id=user_role.role_id)
        session.add(new_user_role)
        session.commit()
        session.refresh(new_user_role)
        return new_user_role
    except Exception as e:
        print("add_user_role() SQL Error: ", e)
        return None
    finally:
        session.close()


async def get_user_role_by_id(user_role_id):
    try:
        query = select(UserRole).where(UserRole.user_role_id == user_role_id)
        result = session.exec(query).first()
        if result:
            return result
        return None
    except Exception as e:
        print("SQL Error: ", e)
        return None
    finally:
        session.close()


async def update_user_role(user_role: UserRoleUpdate):
    try:
        query = select(UserRole).where(UserRole.user_role_id == user_role.user_role_id)
        user_role = session.exec(query).first()
        if user_role:
            user_role.user_id = user_role.user_id
            user_role.role_id = user_role.role_id
            session.commit()
            session.refresh(user_role)
            return True
        return None
    except Exception as e:
        print("SQL Error: ", e)
        return None
    finally:
        session.close()


async def delete_user_role(user_role_id):
    try:
        query = select(UserRole).where(UserRole.user_role_id == user_role_id)
        user_role = session.exec(query).first()
        if user_role:
            session.delete(user_role)
            session.commit()
            return True
        return None
    except Exception as e:
        print("SQL Error: ", e)
        return None
    finally:
        session.close()
