from fastapi import APIRouter, HTTPException

from app.crud.role_perms import list_role_permissions, add_role_permission, update_role_permission, \
    delete_role_permissions
from app.schemas.response import SuccessResponse

router = APIRouter()


@router.get("/list", summary="查看角色权限")
async def root(role_id: int):
    result = await list_role_permissions(role_id)
    if result:
        return SuccessResponse(data=result)
    raise HTTPException(status_code=404, detail="角色权限不存在")


@router.post("/create", summary="添加角色权限")
async def root(role_id: int, permission_id: int):
    result = await add_role_permission(role_id, permission_id)
    if result:
        return SuccessResponse(data=result)
    raise HTTPException(status_code=404, detail="角色权限添加失败")


@router.put("/update", summary="更新角色权限")
async def root(role_permission_id: int, role_id: int, permission_id: int):
    result = await update_role_permission(role_permission_id, role_id, permission_id)
    if result:
        return SuccessResponse(data=result)
    raise HTTPException(status_code=404, detail="角色权限更新失败")


@router.delete("/delete", summary="删除角色权限")
async def root(role_permission_id: int):
    result = await delete_role_permissions(role_permission_id)
    if result:
        return SuccessResponse()
    raise HTTPException(status_code=404, detail="角色权限删除失败")
