# 字典接口
from fastapi import APIRouter

from app.schemas.response import SuccessResponse

router = APIRouter()


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
