from pydantic import BaseModel


class UserRoleCreate(BaseModel):
    user_id: int
    role_id: int


class UserRoleUpdate(BaseModel):
    user_role_id: int | None = None
    user_id: int
    role_id: int
