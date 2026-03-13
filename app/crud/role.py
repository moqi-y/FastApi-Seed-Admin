from datetime import datetime

from sqlalchemy import delete
from sqlmodel import Session, select
from app.crud.database import engine
from app.models.role import Role
from app.models.user_role import UserRole
from app.schemas.role import RoleCreate, RoleUpdate

session = Session(engine)


async def get_roles_list(pageNum, pageSize, keywords):
    """获取角色列表"""
    try:
        roles = session.query(Role)
        if keywords:
            roles = roles.where(Role.name.like(f'%{keywords}%'))
        roles = roles.all()
        total = len(roles)
        roles = roles[(pageNum - 1) * pageSize:pageNum * pageSize]
        return {
            "total": total,
            "list": roles
        }
    except Exception as e:
        print("SQL_Error:", e)
        return None
    finally:
        session.close()


# 通过角色名获取角色信息
async def get_role_by_name(name):
    try:
        role = session.query(Role).filter(Role.name == name).first()
        return role
    except Exception as e:
        print("SQL_Error:", e)
        return None
    finally:
        session.close()


# 角色下拉列表

async def get_roles_options():
    try:
        roles = session.query(Role).all()
        return roles
    except Exception as e:
        print("SQL_Error:", e)
        return None
    finally:
        session.close()


# 查询用户的所有角色编码
async def get_user_roles_codes(user_id: int):
    """获取用户角色编码"""
    try:
        stmt = (
            select(Role.code)  # 只选 role_code
            .join(UserRole, Role.roleId == UserRole.role_id)  # 联表：角色 和 用户角色
            .where(UserRole.user_id == user_id)  # 条件：用户ID
        )
        result = session.exec(stmt)  # 执行 SQL
        return result.all()
    except Exception as e:
        print("SQL_Error:", e)
        return None
    finally:
        session.close()


# 根据role_id获取角色信息
async def get_role_by_id(role_id):
    try:
        query = select(Role).where(Role.roleId == role_id)
        role = session.exec(query).first()
        return role
    except Exception as e:
        print("SQL_Error:", e)
        return None
    finally:
        session.close()


# 根据role_code获取角色信息
async def get_role_by_code(role_code):
    try:
        query = select(Role).where(Role.code == role_code)
        role = session.exec(query).first()
        return role
    except Exception as e:
        print("SQL_Error:", e)
        return None
    finally:
        session.close()


async def add_role(roles: RoleCreate):
    """添加角色"""
    try:
        # 判断角色名是否已存在
        query = select(Role).where(Role.name == roles.name)
        role = session.exec(query).first()
        if role:
            return None
        role = Role(
            name=roles.name,
            code=roles.name,
            status=roles.status,
            desc=roles.description
        )
        session.add(role)
        session.commit()
        session.refresh(role)
        return role
    except Exception as e:
        print("SQL_Error:", e)
        return None
    finally:
        session.close()


async def update_role(new_role: RoleUpdate, role_id):
    """更新角色"""
    try:
        query = select(Role).where(Role.roleId == role_id)
        role = session.exec(query).first()
        if not role:
            return None
        role.name = new_role.name if new_role.name else role.name
        role.description = new_role.description if new_role.description else role.description
        role.updateTime = datetime.now()
        session.commit()
        session.refresh(role)
        return role
    except Exception as e:
        print("SQL_Error:", e)
        return None
    finally:
        session.close()


async def delete_roles(role_ids: list):
    """删除角色"""
    try:
        for role_id in role_ids:
            stmt = delete(Role).where(Role.roleId == role_id)
            session.exec(stmt)
        session.commit()
        return True
    except Exception as e:
        print("SQL_Error:", e)
        return None
    finally:
        session.close()
