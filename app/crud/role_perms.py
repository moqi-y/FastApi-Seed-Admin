from fastapi import HTTPException, status
from sqlalchemy import insert, update, delete
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


async def get_role_menu_ids(role_id):
    try:
        query = select(RolePermission.permission_id).where(RolePermission.role_id == role_id)
        role_permissions = session.exec(query).all()
        return role_permissions
    except Exception as e:
        print("SQL Error: ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="获取用户权限失败")
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


async def update_role_permission(role_id, permission_ids: list[int]):
    """
    更新角色权限
    有则更新，没有则新增
    :param role_id: 角色id
    :param permission_ids: 权限id列表
    """
    try:
        batch_data = [
            {"role_id": role_id, "permission_id": item} for item in permission_ids
        ]
        query = select(RolePermission).where(RolePermission.role_id == role_id)
        role_permission = session.exec(query).first()
        if not role_permission:
            stmt = insert(RolePermission).values(batch_data)
            session.exec(stmt)
            session.commit()
            return True
        else:
            delete_stmt = delete(RolePermission).where(RolePermission.role_id == role_id)
            session.exec(delete_stmt)
            stmt = insert(RolePermission).values(batch_data)
            session.exec(stmt)
            session.commit()
            return True
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
