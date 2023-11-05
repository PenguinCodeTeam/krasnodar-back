from internal.repositories.db.helpers import connection_string
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


_engine = create_async_engine(connection_string)


def get_session_maker():
    return async_sessionmaker(
        _engine,
        autoflush=False,
        expire_on_commit=False,
    )
