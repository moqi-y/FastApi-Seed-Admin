from datetime import datetime

from sqlmodel import Session, select

from app.crud.database import engine
from app.models.permission import Perm
from app.models.role_permission import RolePermission
from app.models.user_role import UserRole
from app.schemas.perm import PermCreate, PermUpdate

session = Session(engine)


async def get_perms_list(pageNum: int, pageSize: int, keyword: str | None = None):
    try:
        perms = session.query(Perm)
        if keyword:
            perms = perms.filter(Perm.permission_name.like(f"%{keyword}%"))
        perms = perms.all()
        total = len(perms)
        perms = perms[(pageNum - 1) * pageSize:pageNum * pageSize]
        return {
            "total": total,
            "list": perms
        }
    except Exception as e:
        print(e)
        return None
    finally:
        session.close()


# 根据permission_id获取权限信息
async def get_perm_by_id(permission_id):
    try:
        query = select(Perm).where(Perm.permission_id == permission_id)
        perm = session.exec(query).first()
        return perm
    except Exception as e:
        print("SQL_Error:", e)
        return None
    finally:
        session.close()


# 查询用户的所有权限编码
async def get_user_perm_codes(user_id: int):
    try:
        stmt = (
            select(Perm.code)  # 只选权限编码
            .distinct()  # 去重
            .join(RolePermission, Perm.permission_id == RolePermission.permission_id)  # 联表：权限 和 角色权限
            .join(UserRole, RolePermission.role_id == UserRole.role_id)  # 联表：角色权限 和 用户角色
            .where(UserRole.user_id == user_id)  # 条件：用户ID
        )
        result = session.exec(stmt)
        return result.all()
    except Exception as e:
        print("SQL_Error:", e)
        return None
    finally:
        session.close()


# 查询权限列表
async def add_perm(perms: PermCreate):
    try:
        # 查询权限是否存在
        query = select(Perm).where(Perm.permission_name == perms.permission_name)
        perm = session.exec(query).first()
        if perm:
            return None
        new_perm = Perm(
            permission_name=perms.permission_name,
            permission_code=perms.permission_code,
            permission_type=perms.permission_type,
            permission_desc=perms.permission_desc
        )
        session.add(new_perm)
        session.commit()
        session.refresh(new_perm)
        return new_perm
    except Exception as e:
        print("SQL_Error:", e)
        return None
    finally:
        session.close()


async def update_perm(perms: PermUpdate):
    try:
        query = select(Perm).where(Perm.permission_id == perms.permission_id)
        perm = session.exec(query).first()
        if perm:
            perm.permission_name = perms.permission_name
            perm.permission_desc = perms.permission_desc
            perm.update_time = datetime.now()
            session.commit()
            session.refresh(perm)
            return perm
        return None
    except Exception as e:
        print("SQL_Error:", e)
        return None
    finally:
        session.close()


async def delete_perm(permission_id: int):
    try:
        query = select(Perm).where(Perm.permission_id == permission_id)
        perm = session.exec(query).first()
        if perm:
            session.delete(perm)
            session.commit()
            return perm
        return None
    except Exception as e:
        print("SQL_Error:", e)
        return None
    finally:
        session.close()
