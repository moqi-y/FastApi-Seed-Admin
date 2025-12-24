from datetime import datetime

from pydantic import BaseModel


class Role(BaseModel):
    role_id: int
    role_name: str
    role_code: str
    role_status: int | None = None
    role_desc: str
    create_time: datetime
    update_time: datetime


class RoleCreate(BaseModel):
    role_name: str
    role_code: str
    role_status: int | None = None
    role_desc: str


class RoleUpdate(BaseModel):
    role_name: str
    role_code: str
    role_status: int | None = None
    role_desc: str
