from fastapi import APIRouter, HTTPException

from app.crud.menu import get_menu
from app.schemas.response import SuccessResponse

router = APIRouter()


@router.get("/routes")
async def root():
    result = await get_menu()
    if not result:
        raise HTTPException(status_code=400, detail="获取菜单出错")
    return SuccessResponse(code="00000", data=result)
