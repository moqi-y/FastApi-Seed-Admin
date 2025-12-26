from datetime import datetime

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    username: str
    nickname: str
    avatar: str | None
    password: str
    email: str | None


class UserOut(BaseModel):
    user_id: int | None
    username: str
    email: str | None
    created_at: datetime | None

    class Config:
        # 是否从属性中获取配置
        from_attributes = True
        # 允许未声明的属性
        extra = "allow"


class UserIn(BaseModel):
    user_id: int | None
    username: str
    password: str
    email: str | None


# 个人中心修改用户信息
class UserUpdate(BaseModel):
    id: int | None = None
    username: str | None = None
    nickname: str | None = None
    avatar: str | None = None
    gender: int | None = None
    mobile: str | None = None
    email: str | None = None


class PasswordUpdate(BaseModel):
    oldPassword: str
    newPassword: str


class EmailUpdate(BaseModel):
    email: str
    code: str


class QueryUserPage(BaseModel):
    """页码"""
    pageNum: int
    """每页记录数"""
    pageSize: int
    """创建时间范围"""
    created_at: str | None = None
    """部门ID"""
    dept_id: str | None = None
    """排序方式（正序:ASC；反序:DESC）"""
    direction: str | None = None
    """排序的字段"""
    field: str | None = None
    """关键字(用户名/昵称/手机号)"""
    keywords: str | None = None
    """角色ID"""
    role_ids: str | None = None
    """用户状态"""
    status: str | None = None
