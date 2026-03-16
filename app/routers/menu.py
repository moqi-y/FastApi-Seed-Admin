from fastapi import APIRouter, HTTPException

from app.crud.menu import get_menu
from app.crud.permission import get_perm_options
from app.schemas.response import SuccessResponse

router = APIRouter()


@router.get("/routes")
async def root():
    result = await get_menu()
    if not result:
        raise HTTPException(status_code=400, detail="获取菜单出错")
    return SuccessResponse(code="00000", data=result)


# 菜单下拉列表
@router.get("/options")
async def root():
    result = await get_perm_options()
    if not result:
        raise HTTPException(status_code=400, detail="获取菜单出错")
    return SuccessResponse(code="00000", data=result)
