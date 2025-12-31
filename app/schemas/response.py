from typing import Any, List

from pydantic import BaseModel


# 定义一个成功响应的类
class SuccessResponse(BaseModel):
    """
    - code: int = 00000  # 定义响应码为00000
    - message: str = "操作成功"  # 定义响应消息
    - data: Any  # 定义响应数据为任意类型
    """
    code: int | str = '00000'  # 定义响应码为200
    message: str = "操作成功"  # 定义响应消息
    data: Any = None  # 定义响应数据为任意类型


# 定义一个失败响应的类
class ErrorResponse(BaseModel):
    """
    - code: int = 500  # 定义响应码
    - message: str = "操作失败"  # 定义响应消息
    """
    code: int | str = 500  # 定义响应码
    message: str = "操作失败"  # 定义响应消息


class PageData(BaseModel):
    total: int = 0  # 定义总条数
    list: Any = []  # 定义列表数据


# 定义一个分页响应的类
class PaginationResponse(BaseModel):
    """
    - code: int = "00000"        # 定义响应码为"00000"
    - message: str = "操作成功"  # 定义响应消息为success
    - data: PageData | None = None  # 定义响应数据为PageDate类型
        * PageData[total]: int  # 定义总条数
        * PageData[list]: Any  # 定义列表数据
    """
    code: int | str = "00000"  # 定义响应码为00000
    message: str = "操作成功"  # 定义响应消息为success
    data: PageData = PageData()  # 定义响应数据为任意类型
