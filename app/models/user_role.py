from datetime import datetime

from sqlmodel import SQLModel, Field


class UserRole(SQLModel, table=True):
    """用户角色表"""
    __tablename__ = "sys_role_user"
    user_role_id: int = Field(default=None, primary_key=True, description="用户角色ID")
    user_id: int = Field(foreign_key="sys_user.user_id")
    role_id: int = Field(foreign_key="sys_role.role_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
