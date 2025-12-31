from typing import List

from sqlmodel import Session, select, or_, delete
from app.crud.database import engine
from app.models.dict import Dict
from app.schemas.dict import AddDict

session = Session(engine)


async def get_dict_list(pageNum, pageSize, keywords):
    """
    根据分页参数和关键词获取字典列表
    参数:
        pageNum: 页码
        pageSize: 每页记录数
        keyword: 搜索关键词
    返回:
        tuple: (总记录数, 当前页记录列表)
    """
    try:
        # 构建基础查询语句
        stmt = select(Dict)
        # 如果有关键词，添加查询条件
        if keywords:
            stmt = stmt.where(or_(Dict.name.like(f"%{keywords}%"), Dict.dictCode.like(f"%{keywords}%")))
            # 在名称或字典代码中模糊匹配关键词
        total = len(session.exec(stmt).all())
        # 计算总记录数
        records = session.exec(stmt.limit(pageSize).offset((pageNum - 1) * pageSize)).all()
        # 分页查询记录
        return total, records
    except Exception as e:
        print("get_dict_list() SQL Error: ", e)
        # 打印错误信息
    finally:
        session.close()
        # 确保会话被关闭


# 新增字典
async def add_dict(dict_data: AddDict):
    try:
        new_dict = Dict(name=dict_data.name, dictCode=dict_data.dictCode, status=dict_data.status,
                        remark=dict_data.remark)
        session.add(new_dict)
        session.commit()
        session.refresh(new_dict)
        return True
    except Exception as e:
        session.rollback()
        print("add_dict() SQL Error: ", e)
    finally:
        session.close()


# 删除字典
async def delete_dict(dict_id: List[int]):
    try:
        for _id in dict_id:
            stmt = delete(Dict).where(Dict.id == _id)
            session.exec(stmt)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print("delete_dict() SQL Error: ", e)
    finally:
        session.close()
