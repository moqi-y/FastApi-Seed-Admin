from sqlmodel import select, Session
from app.core.security import verify_password
from app.crud.database import engine
from app.models.user import User

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
def update_user_info(user_id: int, username: str, password: str, email: str):
    try:
        # 更新用户信息
        result = session.exec(select(User).where(User.id == user_id)).one()
        result.username = username
        result.password = password
        result.email = email
        session.add(result)
        session.commit()
        session.refresh(result)
        return True
    except Exception as e:
        print(f"SQL_Error: {e}")
        return False
    finally:
        session.close()
