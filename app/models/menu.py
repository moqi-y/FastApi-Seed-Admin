from datetime import datetime

from sqlmodel import SQLModel, Field


class Menu(SQLModel, table=True):
    __tablename__ = "sys_menu"
    id: int = Field(default=None, primary_key=True, description="主键 ID")
    parent_id: int = Field(default=0, nullable=True, description="父级菜单ID")
    name: str = Field(description="菜单名称")
    path: str = Field(nullable=True, description="路由地址")
    component: str = Field(nullable=True, description="组件路径")
    redirect: str = Field(nullable=True, description="重定向地址")
    icon: str = Field(nullable=True, description="菜单图标")
    title: str = Field(nullable=True, description="菜单标题")
    hidden: int = Field(default=0, description="是否隐藏（0显示，1隐藏）")
    keep_alive: int = Field(default=1, description="是否缓存（0不缓存，1缓存）")
    always_show: int = Field(default=0, description="是否总是显示（0不显示，1显示）")
    params: str = Field(nullable=True, description="路由参数")
    sort: int = Field(default=0, description="排序")
    created_at: datetime = Field(nullable=True, default=datetime.now())
    updated_at: datetime = Field(nullable=True, default=datetime.now())
    is_deleted: int = Field(default=0, nullable=True, description="是否删除（0未删除，1已删除）")
