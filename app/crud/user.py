from enum import Enum

from sqlmodel import select, Session
from app.core.security import verify_password, hash_password
from app.crud.database import engine
from app.models.user import User
from app.schemas.user import UserUpdate, PasswordUpdate

session = Session(engine)


# 新增用户
def create_user(username: str, nickname: str, avatar: str, password: str, email: str):
    try:
        # 创建用户
        user = User(username=username, nickname=nickname, avatar=avatar, password=password, email=email)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except Exception as e:
        print("SQL_Error:", e)
        return None
    finally:
        session.close()


# 根据用户名查询用户
def get_user_by_username(username: str):
    try:
        # 查询用户，如果不存在则返回 None
        user = session.exec(
            select(User).where(User.username == username)
        ).first()
        return user
    except Exception as e:
        print(f"SQL_Error: {e}")
        return None
    finally:
        session.close()


# 根据用户ID查询用户
def get_user_by_id(user_id: int):
    try:
        # 查询用户，如果不存在则返回 None
        user = session.exec(
            select(User).where(User.user_id == user_id)
        ).first()
        return user
    except Exception as e:
        print(f"SQL_Error: {e}")
        return None
    finally:
        session.close()


# 根据用户名和密码查询用户
def authenticate_user(username: str, password: str):
    try:
        # 从数据库中获取用户信息
        user = get_user_by_username(username=username)
        # 如果用户存在且密码正确，则返回用户信息
        if user and verify_password(password, user.password):
            return user
        # 否则返回None
        return None
    except Exception as e:
        print(f"SQL_Error: {e}")
        return None


# 更新用户信息
async def update_user_info(user: UserUpdate):
    try:
        # 更新用户信息
        result = session.exec(select(User).where(User.user_id == user.id)).one()
        result.username = user.username if user.username is not None else result.username  # 如果用户名不为空，则更新用户名
        result.nickname = user.nickname if user.nickname is not None else result.nickname  # 如果昵称不为空，则更新昵称
        result.avatar = user.avatar if user.avatar is not None else result.avatar
        result.gender = user.gender if user.gender is not None else result.gender
        result.mobile = user.mobile if user.mobile is not None else result.mobile
        result.email = user.email if user.email is not None else result.email
        session.add(result)
        session.commit()
        session.refresh(result)
        return True
    except Exception as e:
        print(f"SQL_Error: {e}")
        return False
    finally:
        session.close()


class PasswordStatus(int, Enum):
    success = 1  # 成功状态
    fail = 2  # 失败状态
    oldPasswordError = 3  # 原始密码错误
    newPasswordError = 4  # 新密码错误
    samePasswordError = 5  # 新密码与原始密码相同


async def update_user_password(password: PasswordUpdate, user_id: int):
    try:
        # 不允许有空格
        if password.newPassword is not None:
            password.newPassword = password.newPassword.strip()
        # 存在性校验
        if password.newPassword is None or password.newPassword == "":
            return PasswordStatus.newPasswordError
        if password.oldPassword is None or password.oldPassword == "":
            return PasswordStatus.oldPasswordError
        # 获取用户信息
        result = session.exec(select(User).where(User.user_id == user_id)).one()
        # 校验原始密码是否正确
        if not verify_password(password.oldPassword, result.password):
            return PasswordStatus.oldPasswordError
            # 校验新密码是否与原始密码一致
        elif verify_password(password.newPassword, result.password):
            return PasswordStatus.samePasswordError
        else:
            # 更新用户密码
            result.password = hash_password(password.newPassword)
            session.add(result)
            session.commit()
            session.refresh(result)
            return PasswordStatus.success
    except Exception as e:
        print(f"SQL_Error: {e}")
        return False
    finally:
        session.close()
