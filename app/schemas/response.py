from typing import Any

from pydantic import BaseModel


# 定义一个成功响应的类
class SuccessResponse(BaseModel):
    """
    - code: int = 200  # 定义响应码为200
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


# 定义一个分页响应的类
class PaginationResponse(BaseModel):
    """
    - code: int = 200           # 定义响应码为200
    - message: str = "操作成功"  # 定义响应消息为success
    - total: int                # 定义总条数
    - list: Any                 # 定义列表数据
    """
    code: int | str = 200  # 定义响应码为200
    message: str = "操作成功"  # 定义响应消息为success
    total: int  # 定义总条数
    list: Any  # 定义列表数据
