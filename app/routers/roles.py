from fastapi import APIRouter, HTTPException

from app.crud.role import (
    add_role,
    delete_roles,
    get_role_by_id,
    get_roles_list,
    get_roles_options,
    update_role,
)
from app.crud.role_perms import get_role_menu_ids, update_role_permission
from app.schemas.response import PageData, PaginationResponse, SuccessResponse
from app.schemas.role import RoleCreate, RoleUpdate
from app.utils.str_to_list import str_to_int_list

router = APIRouter()


@router.get("/options", response_model=SuccessResponse, summary="角色下拉选项")
async def role_options():
    return SuccessResponse(data=await get_roles_options())


@router.get("/page", response_model=PaginationResponse, summary="角色分页")
async def list_roles(pageNum: int = 1, pageSize: int = 10, keywords: str | None = None):
    if pageNum < 1 or not 1 <= pageSize <= 100:
        raise HTTPException(status_code=422, detail="分页参数无效")
    return PaginationResponse(data=PageData(**await get_roles_list(pageNum, pageSize, keywords)))


@router.get("/{role_id}/menuIds", response_model=SuccessResponse, summary="获取角色权限")
async def role_permission_ids(role_id: int):
    return SuccessResponse(data=await get_role_menu_ids(role_id))


@router.put("/{role_id}/menus", response_model=SuccessResponse, summary="分配角色权限")
async def set_role_permissions(role_id: int, permission_ids: list[int]):
    result = await update_role_permission(role_id, permission_ids)
    if not result:
        raise HTTPException(status_code=400, detail="更新角色权限失败")
    return SuccessResponse()


@router.get("/{role_id}/form", response_model=SuccessResponse, summary="角色详情")
async def role_form(role_id: int):
    role = await get_role_by_id(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")
    return SuccessResponse(data=role)


@router.post("", response_model=SuccessResponse, summary="新建角色")
async def create_role(data: RoleCreate):
    role = await add_role(data)
    if not role:
        raise HTTPException(status_code=409, detail="角色名称或编码已存在")
    return SuccessResponse(data=role)


@router.put("/{role_id}", response_model=SuccessResponse, summary="更新角色")
async def edit_role(role_id: int, data: RoleUpdate):
    role = await update_role(data, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在或编码重复")
    return SuccessResponse(data=role)


@router.delete("/{role_ids}", response_model=SuccessResponse, summary="删除角色")
async def remove_roles(role_ids: str):
    if not await delete_roles(str_to_int_list(role_ids)):
        raise HTTPException(status_code=409, detail="系统管理员角色不能删除")
    return SuccessResponse()
