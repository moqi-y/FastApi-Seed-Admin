from datetime import datetime

from sqlmodel import Session, select

from app.crud.database import engine
from app.models.menu import Menu
from app.schemas.menu import flat_to_tree

session = Session(engine)


# 获取菜单路由列表
async def get_menu():
    try:
        menus = session.exec(select(Menu)).all()
        # 转换为list
        menus = [menu.dict() for menu in menus]
        tree = flat_to_tree(menus)
        return tree
    except Exception as e:
        print(e)
        return []
    finally:
        session.close()


# 获取菜单路由列表
async def get_menu_by_id(id):
    try:
        menu = session.exec(select(Menu).where(Menu.id == id)).one()
        return menu
    except Exception as e:
        print(e)
        return None
    finally:
        session.close()


# 更新菜单路由列表
async def update_menu(id, name, path, component, parent_id, hidden, sort, icon, create_time, update_time):
    try:
        menu = session.exec(select(Menu).where(Menu.id == id)).one()
        menu.name = name
        menu.path = path
        menu.component = component
        menu.parent_id = parent_id
        menu.hidden = hidden
        menu.sort = sort
        menu.icon = icon
        menu.create_time = create_time
        menu.update_time = update_time
        session.add(menu)
        session.commit()
        session.refresh(menu)
        return menu
    except Exception as e:
        print(e)
        return None
    finally:
        session.close()


# 删除菜单路由列表
async def delete_menu(id):
    try:
        menu = session.exec(select(Menu).where(Menu.id == id)).one()
        menu.is_deleted = 1
        session.commit()
        session.refresh(menu)
        return menu
    except Exception as e:
        print(e)
        return None
    finally:
        session.close()
