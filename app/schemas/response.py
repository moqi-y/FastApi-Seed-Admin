from typing import Any

from pydantic import BaseModel, Field


class SuccessResponse(BaseModel):
    code: int | str = "00000"
    message: str = "操作成功"
    data: Any = None


class ErrorResponse(BaseModel):
    code: int | str = 500
    message: str = "操作失败"
    data: Any = None


class PageData(BaseModel):
    total: int = 0
    list: Any = Field(default_factory=list)


class PaginationResponse(BaseModel):
    code: int | str = "00000"
    message: str = "操作成功"
    data: PageData = Field(default_factory=PageData)
