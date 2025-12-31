# 字典接口
from fastapi import APIRouter

from app.crud.dict import get_dict_list, add_dict, delete_dict
from app.schemas.dict import AddDict
from app.schemas.response import SuccessResponse, PaginationResponse, PageData
from app.utils.str_to_list import str_to_int_list

router = APIRouter()


# 字典分页列表
@router.get("/page", summary="字典分页列表")
async def root(pageNum: int = 1, pageSize: int = 10, keywords: str | None = None):
    total, records = await get_dict_list(pageNum, pageSize, keywords)
    return PaginationResponse(
        data=PageData(
            list=records,
            total=total,
        )
    )


# 新增字典
@router.post("", summary="新增字典")
async def root(dict_data: AddDict):
    result = await add_dict(dict_data)
    if result:
        return SuccessResponse()
    else:
        return SuccessResponse(code=400, message="新增失败")


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


# 删除字典
@router.delete("/{dict_id}", summary="删除字典")
async def root(dict_id: str):
    dict_id = str_to_int_list(dict_id)
    result = await delete_dict(dict_id)
    if result:
        return SuccessResponse()
    else:
        return SuccessResponse(code=400, message="删除失败")
