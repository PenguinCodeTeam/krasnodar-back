from contextlib import asynccontextmanager

from internal.repositories.db._session import get_session_maker


class DatabaseRepository:
    def __init__(self):
        self.session_maker = get_session_maker()

    @asynccontextmanager
    async def transaction(self):
        async with self.session_maker() as session:
            async with session.begin():
                yield session
