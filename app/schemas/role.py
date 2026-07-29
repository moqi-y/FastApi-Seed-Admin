from datetime import datetime

from pydantic import BaseModel


class Role(BaseModel):
    role_id: int
    name: str
    code: str
    status: int | None = None
    description: str | None = None
    create_time: datetime
    update_time: datetime


class RoleCreate(BaseModel):
    name: str
    code: str
    status: int | None = None
    description: str | None = None


class RoleUpdate(BaseModel):
    name: str
    code: str
    status: int | None = None
    description: str | None = None
