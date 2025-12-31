from datetime import datetime

from sqlmodel import SQLModel, Field


class DictData(SQLModel, table=True):
    __tablename__ = "sys_dict_data"
    id: int = Field(default=None, primary_key=True)
    dictCode: str = Field(default=None, index=True, sa_column_kwargs={"name": "dict_code"})
    value: str = Field(default=None)
    label: str = Field(default=None)
    sort: int = Field(default=0)
    status: int = Field(default=0, description="0：禁用，1：启用")
    tagType: str = Field(default=None)
