from pydantic import BaseModel


class AddDict(BaseModel):
    name: str
    dictCode: str
    remark: str | None = None
    status: int = 1
