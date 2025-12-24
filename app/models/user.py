from datetime import datetime
from sqlmodel import Field, SQLModel


# 用户类，继承自SQLModel，并指定为数据库表
class User(SQLModel, table=True):
    """系统用户表"""
    __tablename__ = "sys_user"
    # 用户ID，默认为None，为主键,自动生成,此处存在官方库bug,不要使用alias参数，不生效。
    user_id: int | None = Field(default=None, primary_key=True, index=True,description="用户ID")
    # 用户名，设置索引
    username: str = Field(index=True)
    nickname: str | None = None
    avatar: str | None = None
    # 密码，设置索引
    password: str
    # 邮箱，设置索引
    email: str | None = None
    # 创建时间，默认为当前时间25, email='jane.doe@example.com', active=False)
    created_at: datetime = Field(default=datetime.now())
