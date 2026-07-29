from pydantic import BaseModel, Field


class PermCreate(BaseModel):
    parent_id: int = 0
    name: str
    code: str
    type: str | int = "4"
    path: str | None = None
    icon: str | None = None
    sort: int = 0
    status: int = 1
    description: str | None = None


class PermUpdate(PermCreate):
    permission_id: int
