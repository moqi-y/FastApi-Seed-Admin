from pydantic import BaseModel


class PermCreate(BaseModel):
    name: str
    code: str
    description: str


class PermUpdate(BaseModel):
    permission_id: int
    name: str
    code: str
    description: str
