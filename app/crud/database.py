from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine
import os

# 加载 .env 文件
load_dotenv()

# 连接数据库
if os.getenv("SQL_TYPE") and os.getenv("SQL_TYPE") == "mysql":  # 如果SQL_TYPE为mysql，则连接mysql数据库
    # MySql
    DATABASE_URL = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DB')}"
    engine = create_engine(DATABASE_URL, pool_recycle=3600, pool_pre_ping=True, echo=False)
# 如果SQL_TYPE为sqlite，则连接sqlite数据库
elif os.getenv("SQL_TYPE") and os.getenv("SQL_TYPE") == "sqlite":
    # sqlite
    engine = create_engine(f"sqlite:///{os.getenv('SQLITE_FILE')}", echo=True)
else:
    raise Exception("SQL_TYPE in '.env' must be mysql or sqlite")


def create_db_and_tables():
    SQLModel.metadata.create_all(bind=engine)

# 定义一个上下文管理器，用于获取数据库会话
# def get_session():
#     with Session(engine) as session:
#         try:
#             yield session
#         finally:
#             session.close()
