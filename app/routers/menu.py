import json

from fastapi import APIRouter, HTTPException

from app.crud.menu import get_menu, get_menu_by_id
from app.crud.permission import get_perm_options
from app.schemas.response import SuccessResponse

router = APIRouter()


# 菜单列表
@router.get("")
async def root():
    result = await get_perm_options()
    if not result:
        raise HTTPException(status_code=400, detail="获取菜单出错")
    result_dict = result.copy()
    for item in result_dict:
        item["routePath"] = item["path"]
    return SuccessResponse(code="00000", data=result_dict)


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


@router.post("")
async def root(menu: dict):
    result = await add_menu(menu)
    return SuccessResponse(code="00000", data="")


@router.get("/{id}/form")
async def root(id: int):
    result = await get_menu_by_id(id)
    if not result:
        raise HTTPException(status_code=400, detail="获取菜单出错")
    print(result.dict())
    result = result.dict()
    new_rsult = {
        "parentId": result["parent_id"] if result["parent_id"] != 0 else "顶级菜单",
        "visible": result["hidden"],
        "sort": result["sort"],
        "type": 1,  ###
        "alwaysShow": result["always_show"],
        "keepAlive": result["keep_alive"],
        "params": result["params"],
        "name": result["name"],
        # "routeName": result["route_name"],  ###
        "routePath": result["path"],
        "component": result["component"],
        "icon": result["icon"]
    }
    return SuccessResponse(code="00000", data=new_rsult)

# {
#     "parentId": "0",
#     "visible": 1,
#     "sort": 1,
#     "type": 1,
#     "alwaysShow": 0,
#     "keepAlive": 1,
#     "params": [],
#     "name": "菜单名称",
#     "routeName": "路由名称",
#     "routePath": "路由路径",
#     "component": "路由路径",
#     "icon": "bilibili"
# }
