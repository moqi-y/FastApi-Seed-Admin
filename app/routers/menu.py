from fastapi import APIRouter, HTTPException

from app.crud.menu import add_menu, delete_menu, get_menu, get_menu_by_id, update_menu
from app.crud.permission import get_perm_options
from app.schemas.response import SuccessResponse

router = APIRouter()


@router.get("/routes", response_model=SuccessResponse, summary="获取动态路由")
async def routes():
    return SuccessResponse(data=await get_menu())


@router.get("/options", response_model=SuccessResponse, summary="获取权限菜单选项")
async def options():
    return SuccessResponse(data=await get_perm_options())


@router.get("", response_model=SuccessResponse, summary="获取菜单树")
async def list_menus():
    return SuccessResponse(data=await get_menu())


@router.post("", response_model=SuccessResponse, summary="创建菜单")
async def create_menu(menu: dict):
    return SuccessResponse(data=await add_menu(menu))


@router.get("/{menu_id}/form", response_model=SuccessResponse, summary="菜单详情")
async def menu_form(menu_id: int):
    menu = await get_menu_by_id(menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="菜单不存在")
    return SuccessResponse(
        data={
            "parentId": menu.parent_id,
            "visible": 0 if menu.hidden else 1,
            "sort": menu.sort,
            "alwaysShow": menu.always_show,
            "keepAlive": menu.keep_alive,
            "params": menu.params,
            "name": menu.name,
            "routeName": menu.routeName,
            "routePath": menu.path,
            "component": menu.component,
            "redirect": menu.redirect,
            "icon": menu.icon,
        }
    )


@router.put("/{menu_id}", response_model=SuccessResponse, summary="更新菜单")
async def edit_menu(menu_id: int, menu: dict):
    result = await update_menu(menu_id, menu)
    if not result:
        raise HTTPException(status_code=404, detail="菜单不存在")
    return SuccessResponse(data=result)


@router.delete("/{menu_id}", response_model=SuccessResponse, summary="删除菜单")
async def remove_menu(menu_id: int):
    result = await delete_menu(menu_id)
    if not result:
        raise HTTPException(status_code=404, detail="菜单不存在")
    return SuccessResponse(data=result)
