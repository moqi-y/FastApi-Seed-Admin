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
