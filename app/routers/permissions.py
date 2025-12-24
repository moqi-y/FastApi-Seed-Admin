from fastapi import APIRouter, HTTPException

from app.schemas.perm import PermCreate, PermUpdate
from app.schemas.response import *

from app.crud.permission import get_perms_list, add_perm, update_perm, delete_perm

router = APIRouter()


# 查看权限
@router.get("/permissions", summary="查看权限")
async def root(pageNum: int = 1, pageSize: int = 10, keyword: str | None = None):
    perms = await get_perms_list(pageNum, pageSize, keyword)
    if perms:
        return PaginationResponse(total=perms["total"], list=perms["list"])
    raise HTTPException(status_code=404, detail="权限不存在")


# 添加权限
@router.post("/permissions", summary="添加权限")
async def root(perms: PermCreate):
    result = await add_perm(perms)
    if result:
        return SuccessResponse()
    raise HTTPException(status_code=400, detail="添加失败")


# 修改权限
@router.put("/permissions", summary="修改权限")
async def root(perms: PermUpdate):
    result = await update_perm(perms)
    if result:
        return SuccessResponse(data=result)
    raise HTTPException(status_code=400, detail="修改失败")


# 删除权限
@router.delete("/permissions", summary="删除权限")
async def root(permission_id: int):
    result = await delete_perm(permission_id)
    if result:
        return SuccessResponse(data=result, message="删除成功")
    raise HTTPException(status_code=400, detail="删除失败")
