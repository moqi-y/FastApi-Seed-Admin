from fastapi import APIRouter, HTTPException

from app.crud.user_role import get_user_roles, add_user_role, get_user_role_by_id, update_user_role, delete_user_role
from app.schemas.response import SuccessResponse
from app.schemas.user_role import UserRoleCreate, UserRoleUpdate

router = APIRouter()


@router.get("/list", summary="获取用户角色列表")
async def root(user_id: int):
    result = await get_user_roles(user_id)
    if result:
        return SuccessResponse(data=result)
    raise HTTPException(status_code=400, detail="用户角色不存在")


@router.post("/user_roles", summary="创建用户角色")
async def root(user_role: UserRoleCreate):
    result = await add_user_role(user_role)
    if result:
        return SuccessResponse(data=result)
    raise HTTPException(status_code=400, detail="创建失败,请检查参数")


@router.get("/user_roles/{user_role_id}", summary="获取用户角色详情")
async def root(user_role_id: int):
    result = await get_user_role_by_id(user_role_id)
    if result:
        return SuccessResponse(data=result)
    raise HTTPException(status_code=400, detail="用户角色不存在")


@router.put("/user_roles/{user_role_id}", summary="更新用户角色")
async def root(user_roles: UserRoleUpdate):
    result = await update_user_role(user_roles)
    if result:
        return SuccessResponse(data=result)
    raise HTTPException(status_code=400, detail="更新失败,请检查参数")


@router.delete("/user_roles/{user_role_id}", summary="删除用户角色")
async def root(user_role_id: int):
    result = await delete_user_role(user_role_id)
    if result:
        return SuccessResponse()
    raise HTTPException(status_code=400, detail="用户角色不存在")
