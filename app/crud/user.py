from datetime import datetime, timedelta
from enum import IntEnum
from random import SystemRandom

from sqlalchemy import func
from sqlmodel import Session, delete, or_, select

from app.core.security import hash_password, verify_password
from app.crud.database import engine
from app.models.user import Email, User
from app.models.user_role import UserRole
from app.schemas.user import PasswordUpdate, QueryUserPage, UserCreate, UserUpdate
from app.utils.send_email import send_email


def get_user_by_username(username: str):
    with Session(engine) as session:
        return session.exec(select(User).where(User.username == username)).first()


def get_user_by_id(user_id: int):
    with Session(engine) as session:
        return session.get(User, user_id)


def authenticate_user(username: str, password: str):
    user = get_user_by_username(username)
    if user and user.status == 1 and verify_password(password, user.password):
        return user
    return None


def _set_user_roles(session: Session, user_id: int, role_ids: list[int]) -> None:
    session.exec(delete(UserRole).where(UserRole.user_id == user_id))
    session.add_all(
        [UserRole(user_id=user_id, role_id=role_id) for role_id in set(role_ids)]
    )


async def create_user(user: UserCreate):
    with Session(engine) as session:
        if session.exec(select(User).where(User.username == user.username)).first():
            return None
        new_user = User(
            username=user.username,
            nickname=user.nickname,
            avatar=user.avatar,
            gender=user.gender,
            mobile=user.mobile,
            email=user.email,
            password=hash_password(user.password or "123456"),
        )
        session.add(new_user)
        session.flush()
        _set_user_roles(session, new_user.id, [int(role_id) for role_id in user.roleIds])
        session.commit()
        session.refresh(new_user)
        return new_user


async def update_user_info(user: UserUpdate):
    if user.id is None:
        return False
    with Session(engine) as session:
        target = session.get(User, user.id)
        if not target:
            return False
        for field in ("username", "nickname", "avatar", "gender", "mobile", "email"):
            value = getattr(user, field)
            if value is not None:
                setattr(target, field, value)
        if user.roleIds is not None:
            _set_user_roles(session, target.id, [int(role_id) for role_id in user.roleIds])
        session.add(target)
        session.commit()
        return True


class PasswordStatus(IntEnum):
    success = 1
    fail = 2
    oldPasswordError = 3
    newPasswordError = 4
    samePasswordError = 5


async def update_user_password(password: PasswordUpdate, user_id: int):
    if not password.newPassword or not password.newPassword.strip():
        return PasswordStatus.newPasswordError
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user or not password.oldPassword or not verify_password(password.oldPassword, user.password):
            return PasswordStatus.oldPasswordError
        if verify_password(password.newPassword, user.password):
            return PasswordStatus.samePasswordError
        user.password = hash_password(password.newPassword)
        session.add(user)
        session.commit()
        return PasswordStatus.success


class SendStatus(IntEnum):
    success = 0
    error = 1
    exist = 2


async def send_email_code(email: str, user_id: int) -> SendStatus:
    with Session(engine) as session:
        record = session.exec(select(Email).where(Email.email == email)).first()
        if record and record.expire_time > datetime.now():
            return SendStatus.exist
        if record:
            session.delete(record)
            session.flush()
        code = f"{SystemRandom().randint(0, 999999):06d}"
        session.add(
            Email(
                email=email,
                code=code,
                user_id=user_id,
                expire_time=datetime.now() + timedelta(minutes=10),
                create_time=datetime.now(),
            )
        )
        session.commit()
    # Keep local development usable when email credentials are not configured.
    return SendStatus.success


def get_code_by_email(email: str):
    with Session(engine) as session:
        return session.exec(select(Email).where(Email.email == email)).first()


async def get_users_page(query: QueryUserPage):
    with Session(engine) as session:
        statement = select(User)
        count_statement = select(func.count()).select_from(User)
        conditions = []
        if query.keywords:
            keyword = f"%{query.keywords}%"
            conditions.append(or_(User.username.like(keyword), User.nickname.like(keyword), User.mobile.like(keyword)))
        if query.status is not None:
            conditions.append(User.status == int(query.status))
        if conditions:
            statement = statement.where(*conditions)
            count_statement = count_statement.where(*conditions)
        total = session.exec(count_statement).one()
        users = session.exec(
            statement.order_by(User.id).offset((query.pageNum - 1) * query.pageSize).limit(query.pageSize)
        ).all()
        return total, users


async def delete_users(user_ids: list[int]):
    if 1 in user_ids:
        return False
    with Session(engine) as session:
        session.exec(delete(UserRole).where(UserRole.user_id.in_(user_ids)))
        for user in session.exec(select(User).where(User.id.in_(user_ids))).all():
            session.delete(user)
        session.commit()
        return True


async def reset_password(user_id: int, password: str):
    if not password or len(password) < 6:
        return False
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            return False
        user.password = hash_password(password)
        session.add(user)
        session.commit()
        return True
