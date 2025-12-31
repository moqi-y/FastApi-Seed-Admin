from pydantic import BaseModel


class AddDict(BaseModel):
    name: str
    dictCode: str
    remark: str | None = None
    status: int = 1


class UpdateDict(BaseModel):
    id: int
    name: str
    dictCode: str
    remark: str | None = None
    status: int = 1


class DictItem(BaseModel):
    id: int
    dictCode: str
    value: str
    label: str
    sort: int
    status: int
    tagType: str


class AddDictItem(BaseModel):
    dictCode: str
    value: str
    label: str
    sort: int = 0
    status: int = 1
    tagType: str = 'info'
