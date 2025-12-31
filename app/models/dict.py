from datetime import datetime

from sqlmodel import SQLModel, Field


class Dict(SQLModel, table=True):
    __tablename__ = "sys_dict"
    id: int = Field(default=None, primary_key=True, description="字典ID")
    name: str = Field(description="字典名称")
    dict_code: str = Field(description="字典编码", alias="dictCode")
    remark: str = Field(nullable=True, description="备注")
    status: int = Field(default=1, description="状态（1-启用，0-禁用）")
