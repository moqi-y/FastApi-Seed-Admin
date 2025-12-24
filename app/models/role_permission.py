from datetime import datetime

from sqlmodel import SQLModel, Field


class RolePermission(SQLModel, table=True):
    """角色权限表"""
    __tablename__ = "sys_role_permission"
    id: int = Field(default=None, primary_key=True, description="角色权限ID")
    role_id: int = Field(foreign_key="sys_role.role_id", index=True, description="角色ID")
    permission_id: int = Field(foreign_key="sys_permission.permission_id", description="权限ID")
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
