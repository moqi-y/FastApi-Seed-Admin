# 字典接口
from fastapi import APIRouter, Body, HTTPException

from app.crud.dict import get_dict_list, add_dict, delete_dict, get_dict_form_data, update_dict, add_dict_item, \
    get_dict_item_page, get_dict_item_form, update_dict_item, delete_dict_item
from app.schemas.dict import AddDict, UpdateDict, DictItem, AddDictItem
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


# 字典表单数据
@router.get("/{id}/form", summary="字典表单数据")
async def root(id: int):
    result = await get_dict_form_data(id)
    if result:
        return SuccessResponse(data=result)
    else:
        raise HTTPException(status_code=400, detail="获取失败")


# 新增字典
@router.post("", summary="新增字典")
async def root(dict_data: AddDict):
    result = await add_dict(dict_data)
    if result:
        return SuccessResponse()
    else:
        raise HTTPException(status_code=400, detail="新增失败")


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


# 修改字典
@router.put("/{dict_id}", summary="修改字典")
async def root(dict_id: str, dict_data: UpdateDict = Body(...)):
    result = await update_dict(dict_id, dict_data)
    if result:
        return SuccessResponse()
    else:
        raise HTTPException(status_code=400, detail="修改失败")


# 删除字典
@router.delete("/{dict_id}", summary="删除字典")
async def root(dict_id: str):
    dict_id = str_to_int_list(dict_id)
    result = await delete_dict(dict_id)
    if result:
        return SuccessResponse()
    else:
        raise HTTPException(status_code=400, detail="删除失败")


"""字典项"""


# 新增字典项
@router.post("/{dict_code}/items", summary="新增字典项")
async def root(dict_code: str, dict_item: AddDictItem = Body(...)):
    result = await add_dict_item(dict_code, dict_item)
    if result:
        return SuccessResponse()
    else:
        raise HTTPException(status_code=400, detail="新增失败")


# 字典项分页列表
@router.get("/{dict_code}/items/page", summary="字典项分页列表")
async def root(dict_code: str, pageNum: int = 1, pageSize: int = 10, keywords: str = None):
    total, records = await get_dict_item_page(dict_code, pageNum, pageSize, keywords)
    return PaginationResponse(data=PageData(total=total, list=records))


# 字典项表单数据
@router.get("/{dict_code}/items/{itemId}/form", summary="字典项表单数据")
async def root(dict_code: str, itemId: str):
    result = await get_dict_item_form(dict_code, itemId)
    if result:
        return SuccessResponse(data=result)
    else:
        raise HTTPException(status_code=400, detail="获取失败")


# 修改字典项
@router.put("/{dict_code}/items/{itemId}", summary="修改字典项")
async def root(dict_code: str, itemId: str, dict_item: DictItem = Body(...)):
    result = await update_dict_item(dict_code, itemId, dict_item)
    if result:
        return SuccessResponse()
    else:
        raise HTTPException(status_code=400, detail="修改失败")


# 删除字典项
@router.delete("/{dict_code}/items/{itemId}", summary="删除字典项")
async def root(dict_code: str, itemId: str):
    result = await delete_dict_item(dict_code, itemId)
    if result:
        return SuccessResponse()
    else:
        raise HTTPException(status_code=400, detail="删除失败")
