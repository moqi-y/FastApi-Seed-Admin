from pydantic import BaseModel


class PermCreate(BaseModel):
    permission_name: str
    permission_code: str
    permission_type: int
    permission_desc: str


class PermUpdate(BaseModel):
    permission_id: int
    permission_name: str
    permission_code: str
    permission_type: int
    permission_desc: str
