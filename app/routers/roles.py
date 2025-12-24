from fastapi import APIRouter, HTTPException

from app.crud.role import get_roles_list, add_role, update_role, delete_role
from app.schemas.response import *
from app.schemas.role import RoleCreate, RoleUpdate

router = APIRouter()


# 分页查找角色
@router.get("/roles", summary="分页查找角色")
async def root(pageNum: int = 1, pageSize: int = 10, keyword: str | None = None):
    roles = await get_roles_list(pageNum, pageSize, keyword)
    if roles:
        return PaginationResponse(total=roles["total"], list=roles["list"])
    raise HTTPException(status_code=400, detail="未找到角色")


# 新建角色
@router.post("/roles", summary="新建角色")
async def root(roles: RoleCreate):
    # 查找是否存在相同名字的角色
    result = await add_role(roles)
    if result:
        return SuccessResponse(message="创建成功", data=result)
    raise HTTPException(status_code=400, detail="创建失败")


# 更新角色
@router.put("/roles", summary="更新角色")
async def root(roles: RoleUpdate):
    result = await update_role(roles)
    if result:
        return SuccessResponse(message="更新成功", data=result)
    raise HTTPException(status_code=400, detail="更新失败, 角色不存在")


# 删除角色
@router.delete("/roles", summary="删除角色")
async def root(role_id: int):
    result = await delete_role(role_id)
    if result:
        return SuccessResponse(message="删除成功", data=result)
    raise HTTPException(status_code=400, detail="删除失败, 角色不存在")
