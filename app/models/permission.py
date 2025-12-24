from datetime import datetime

from sqlmodel import SQLModel, Field


class Perm(SQLModel, table=True):
    """权限表"""
    __tablename__ = "sys_permission"
    permission_id: int = Field(default=None, primary_key=True, index=True, description="权限ID")
    parent_id: int = Field(default=None, description="父级ID")
    name: str = Field(default=None, description="权限名称")
    code: str = Field(default=None, description="权限编码（后端鉴权用，唯一）")
    type: str = Field(default=None, description="权限类型，M=目录/菜单 C=按钮")
    path: str = Field(default=None, description="路径")
    icon: str = Field(default=None, description="图标")
    sort: int = Field(default=0, description="排序")
    status: int = Field(default=1, description="状态 0=正常 1=停用")
    desc: str = Field(default=None, description="权限描述")
    create_time: datetime = Field(default=datetime.now(), description="创建时间")
    update_time: datetime = Field(default=datetime.now(), description="更新时间")
