from sqlmodel import Session, select

from app.crud.database import engine
from app.models.role_permission import RolePermission

session = Session(engine)


async def list_role_permissions(role_id):
    try:
        query = select(RolePermission).where(RolePermission.role_id == role_id)
        role_permissions = session.exec(query).all()
        return role_permissions
    except Exception as e:
        print("SQL Error: ", e)
        return None
    finally:
        session.close()

# 联表查询角色权限
# async def get_role_permission(role_id, permission_id):


async def add_role_permission(role_id, permission_id):
    try:
        query = select(RolePermission).where(RolePermission.role_id == role_id,
                                             RolePermission.permission_id == permission_id)
        role_permission = session.exec(query).first()
        if role_permission:
            return None
        new_role_permission = RolePermission(role_id=role_id, permission_id=permission_id)
        session.add(new_role_permission)
        session.commit()
        session.refresh(new_role_permission)
        return new_role_permission
    except Exception as e:
        print("SQL Error: ", e)
        return None
    finally:
        session.close()


async def update_role_permission(role_permission_id, role_id, permission_id):
    try:
        query = select(RolePermission).where(RolePermission.role_permission_id == role_permission_id)
        role_permission = session.exec(query).first()
        if not role_permission:
            return None
        role_permission.role_id = role_id
        role_permission.permission_id = permission_id
        session.commit()
        session.refresh(role_permission)
        return role_permission
    except Exception as e:
        print("SQL Error: ", e)
        return None
    finally:
        session.close()


async def delete_role_permissions(role_permission_id):
    try:
        query = select(RolePermission).where(RolePermission.role_permission_id == role_permission_id)
        role_permission = session.exec(query).first()
        if not role_permission:
            return None
        session.delete(role_permission)
        session.commit()
        return True
    except Exception as e:
        print("SQL Error: ", e)
        return None
    finally:
        session.close()
