from fastapi import APIRouter, HTTPException

from app.crud.permission import add_perm, delete_perm, get_perms_list, update_perm
from app.schemas.perm import PermCreate, PermUpdate
from app.schemas.response import PageData, PaginationResponse, SuccessResponse

router = APIRouter()


@router.get("/permissions", response_model=PaginationResponse, summary="查询权限")
async def list_permissions(pageNum: int = 1, pageSize: int = 10, keyword: str | None = None):
    if pageNum < 1 or not 1 <= pageSize <= 100:
        raise HTTPException(status_code=422, detail="分页参数无效")
    result = await get_perms_list(pageNum, pageSize, keyword)
    return PaginationResponse(data=PageData(**result))


@router.post("/permissions", response_model=SuccessResponse, summary="新增权限")
async def create_permission(data: PermCreate):
    result = await add_perm(data)
    if not result:
        raise HTTPException(status_code=409, detail="权限编码已存在")
    return SuccessResponse(data=result)


@router.put("/permissions", response_model=SuccessResponse, summary="修改权限")
async def update_permission(data: PermUpdate):
    result = await update_perm(data)
    if not result:
        raise HTTPException(status_code=404, detail="权限不存在或编码重复")
    return SuccessResponse(data=result)


@router.delete("/permissions/{permission_id}", response_model=SuccessResponse, summary="删除权限")
async def remove_permission(permission_id: int):
    result = await delete_perm(permission_id)
    if not result:
        raise HTTPException(status_code=409, detail="权限不存在或仍有子权限")
    return SuccessResponse(data=result)
