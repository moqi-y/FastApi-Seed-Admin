# 字典接口
from fastapi import APIRouter

from app.crud.dict import get_dict_list
from app.schemas.response import SuccessResponse, PaginationResponse, PageData

router = APIRouter()


# 字典分页列表
@router.get("/page", summary="字典分页列表")
async def root(pageNum: int = 1, pageSize: int = 10, keyword: str | None = None):
    total, records = await get_dict_list(pageNum, pageSize, keyword)
    return PaginationResponse(
        data=PageData(
            list=records,
            total=total,
        )
    )


@router.get("/{dictCode}/items", summary="字典查询")
async def root(dictCode: str):
    # TODO: 查询字典数据
    return SuccessResponse(data=[
        {
            "value": "1",
            "label": "男",
            "tagType": "primary"
        },
        {
            "value": "2",
            "label": "女",
            "tagType": "primary"
        }
    ])
