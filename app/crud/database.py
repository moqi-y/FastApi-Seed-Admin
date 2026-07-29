from urllib.parse import quote_plus

from sqlmodel import Session, SQLModel, create_engine

from app.core.config import get_settings

settings = get_settings()

if settings.sql_type == "mysql":
    database_url = (
        f"mysql+pymysql://{settings.mysql_user}:{quote_plus(settings.mysql_password)}"
        f"@{settings.mysql_host}:{settings.mysql_port}/{settings.mysql_db}"
    )
    engine = create_engine(
        database_url, pool_recycle=3600, pool_pre_ping=True, echo=settings.debug
    )
elif settings.sql_type == "sqlite":
    engine = create_engine(
        f"sqlite:///{settings.sqlite_file}",
        echo=settings.debug,
        connect_args={"check_same_thread": False},
    )
else:
    raise ValueError("SQL_TYPE must be either 'mysql' or 'sqlite'")


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(bind=engine)


def get_session():
    """Yield one short-lived database session per request."""
    with Session(engine) as session:
        yield session
