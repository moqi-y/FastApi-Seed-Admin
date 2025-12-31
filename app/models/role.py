from datetime import datetime

from sqlmodel import SQLModel, Field


class Role(SQLModel, table=True):
    """系统角色表"""
    __tablename__ = "sys_role"
    id: int = Field(default=None, primary_key=True, index=True, description="角色ID",
                    sa_column_kwargs={"name": "role_id"})
    name: str = Field(default=None, description="角色名称", sa_column_kwargs={"name": "role_name"})
    code: str = Field(default=None, description="角色编码", sa_column_kwargs={"name": "role_code"})
    status: int = Field(default=1, description="角色状态", sa_column_kwargs={"name": "role_status"})
    role_desc: str = Field(default=None, description="角色描述")
    createTime: datetime = Field(default=datetime.now(), description="创建时间",
                                 sa_column_kwargs={"name": "create_time"})
    updateTime: datetime = Field(default=datetime.now(), description="更新时间",
                                 sa_column_kwargs={"name": "update_time"})
