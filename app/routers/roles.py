from fastapi import APIRouter, HTTPException

from app.crud.role import get_roles_list, add_role, update_role, get_roles_options, get_role_by_id, \
    delete_roles
from app.crud.role_perms import update_role_permission, get_role_menu_ids
from app.schemas.response import *
from app.schemas.role import RoleCreate, RoleUpdate
from app.utils.str_to_list import str_to_int_list

router = APIRouter()


# 分页查找角色
@router.get("/page", summary="分页查找角色")
async def root(pageNum: int = 1, pageSize: int = 10, keywords: str | None = None):
    roles = await get_roles_list(pageNum, pageSize, keywords)
    if roles:
        return PaginationResponse(data=PageData(**roles))
    raise HTTPException(status_code=400, detail="未找到角色")


# 根据角色ID查找角色
@router.get("/{role_id}/form", summary="根据角色ID查找角色")
async def root(role_id: int):
    roles = await get_role_by_id(role_id)
    if roles:
        return SuccessResponse(message="查询成功", data=roles)
    raise HTTPException(status_code=400, detail="未找到角色")


# 新建角色
@router.post("", summary="新建角色")
async def root(roles: RoleCreate):
    # 查找是否存在相同名字的角色
    result = await add_role(roles)
    if result:
        return SuccessResponse(message="创建成功", data=result)
    raise HTTPException(status_code=400, detail="创建失败")


# 更新角色
@router.put("/{role_id}", summary="更新角色")
async def root(roles: RoleUpdate, role_id: int):
    result = await update_role(roles, role_id)
    if result:
        return SuccessResponse(message="更新成功", data=result)
    raise HTTPException(status_code=400, detail="更新失败, 角色不存在")


# 删除角色
@router.delete("/{role_ids}", summary="删除角色")
async def root(role_ids: str):
    role_id_list = str_to_int_list(role_ids)
    result = await delete_roles(role_id_list)
    if result:
        return SuccessResponse(message="删除成功")
    raise HTTPException(status_code=400, detail="删除失败, 角色不存在")


# 角色下拉列表
@router.get("/options", summary="角色下拉列表")
async def root():
    result = await get_roles_options()
    if result:
        return SuccessResponse(message="查询成功", data=result)
    raise HTTPException(status_code=400, detail="查询失败")


# 权限分配
@router.put("/{role_id}/menus", summary="用户权限分配")
async def root(role_id: int, permissions: List[int]):
    print("role_id：", role_id, " permissions：", permissions)
    result = await update_role_permission(role_id, permissions)
    if result:
        return SuccessResponse(message="更新成功")


# 获取角色菜单权限
@router.get("/{role_id}/menuIds", summary="获取角色菜单权限")
async def root(role_id: int):
    result = await get_role_menu_ids(role_id)
    if result:
        return SuccessResponse(message="查询成功", data=result)
