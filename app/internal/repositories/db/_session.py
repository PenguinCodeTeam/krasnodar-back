import config
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


connection_string = URL.create(
    drivername='postgresql+asyncpg',
    username=config.POSTGRES_USER,
    password=config.POSTGRES_PASSWORD,
    database=config.POSTGRES_DB,
    host=config.POSTGRES_HOST,
    port=config.POSTGRES_PORT,
)

_engine = create_async_engine(connection_string)


def get_session_maker():
    return async_sessionmaker(
        _engine,
        autoflush=False,
        expire_on_commit=False,
    )
