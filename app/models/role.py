from datetime import datetime

from sqlmodel import SQLModel, Field


class Role(SQLModel, table=True):
    """系统角色表"""
    __tablename__ = "sys_role"
    role_id: int = Field(default=None, primary_key=True, index=True, description="角色ID")
    role_name: str = Field(default=None, description="角色名称")
    role_code: str = Field(default=None, description="角色编码")
    role_status: int = Field(default=1, description="角色状态")
    role_desc: str = Field(default=None, description="角色描述")
    create_time: datetime = Field(default=datetime.now(), description="创建时间")
    update_time: datetime = Field(default=datetime.now(), description="更新时间")
