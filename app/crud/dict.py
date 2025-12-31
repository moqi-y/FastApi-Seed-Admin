from sqlmodel import Session, select, or_

from app.crud.database import engine
from app.models.dict import Dict

session = Session(engine)


async def get_dict_list(pageNum, pageSize, keyword):
    try:
        stmt = select(Dict)
        if keyword:
            stmt = stmt.where(or_(Dict.name.like(f"%{keyword}%"), Dict.dictCode.like(f"%{keyword}%")))
        total = len(session.exec(stmt).all())
        records = session.exec(stmt.limit(pageSize).offset((pageNum - 1) * pageSize)).all()
        return total, records
    except Exception as e:
        print("get_dict_list() SQL Error: ", e)
    finally:
        session.close()
