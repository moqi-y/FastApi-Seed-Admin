from datetime import datetime

from sqlmodel import Session, select

from app.crud.database import engine
from app.models.menu import Menu
from app.schemas.menu import flat_to_tree


async def get_menu():
    with Session(engine) as session:
        menus = session.exec(
            select(Menu).where(Menu.is_deleted == 0).order_by(Menu.sort, Menu.id)
        ).all()
        return flat_to_tree([menu.model_dump() for menu in menus])


async def get_menu_by_id(menu_id: int):
    with Session(engine) as session:
        return session.get(Menu, menu_id)


async def add_menu(data: dict):
    with Session(engine) as session:
        menu = Menu(
            parent_id=int(data.get("parentId") or 0),
            name=data["name"],
            title=data.get("title") or data["name"],
            path=data.get("routePath"),
            component=data.get("component"),
            redirect=data.get("redirect"),
            icon=data.get("icon"),
            routeName=data.get("routeName") or data["name"],
            hidden=0 if data.get("visible", 1) else 1,
            keep_alive=data.get("keepAlive", 1),
            always_show=data.get("alwaysShow", 0),
            params=data.get("params"),
            sort=data.get("sort", 0),
        )
        session.add(menu)
        session.commit()
        session.refresh(menu)
        return menu


async def update_menu(menu_id: int, data: dict):
    with Session(engine) as session:
        menu = session.get(Menu, menu_id)
        if not menu:
            return None
        mapping = {
            "parentId": "parent_id", "routePath": "path", "routeName": "routeName",
            "keepAlive": "keep_alive", "alwaysShow": "always_show", "visible": "hidden",
        }
        for key, value in data.items():
            field = mapping.get(key, key)
            if hasattr(menu, field):
                value = 0 if key == "visible" and value else (1 if key == "visible" else value)
                setattr(menu, field, value)
        menu.updated_at = datetime.now()
        session.add(menu)
        session.commit()
        session.refresh(menu)
        return menu


async def delete_menu(menu_id: int):
    with Session(engine) as session:
        menu = session.get(Menu, menu_id)
        if not menu:
            return None
        menu.is_deleted = 1
        menu.updated_at = datetime.now()
        session.add(menu)
        session.commit()
        return menu
