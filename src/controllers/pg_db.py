import typing as tp

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine, async_sessionmaker
from sqlalchemy.engine import URL


class AsyncPGController:
    def __init__(self):
        self.async_session_factory = None
        self._engine = None

    async def get_session(self) -> tp.AsyncGenerator[AsyncSession, tp.Any]:
        async with self.async_session_factory() as session:
            yield session

    async def init_orm_objects(self, db_url: URL,
                               pool_size: int = 5,
                               debug_mode: bool = False):
        self._engine: AsyncEngine = create_async_engine(db_url,
                                                        echo=debug_mode,
                                                        pool_size=int(pool_size),
                                                        max_overflow=3)

        self.async_session_factory = async_sessionmaker(self._engine,
                                                        autoflush=False,
                                                        expire_on_commit=False)

    async def on_shutdown(self):
        await self._engine.dispose()
