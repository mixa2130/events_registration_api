from loguru import logger as async_logger
from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base, DeclarativeMeta

from src.config import Secrets, POSTGRES_INDEXES_NAMING_CONVENTION
from src.controllers import AsyncPGController


class AppContext(Secrets):
    def __init__(self):
        super().__init__()

        self.debug = self.DEBUG_MODE
        self.logger = async_logger

        self.pg_controller: AsyncPGController = AsyncPGController()
        self.sa_metadata: MetaData = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION,
                                              schema=self.PG_SCHEMA)
        self.sa_base: DeclarativeMeta = declarative_base(metadata=self.sa_metadata)

    async def on_startup(self):
        await self.pg_controller.init_orm_objects(db_url=self.PG_DSN,
                                                  pool_size=self.PG_POOL_SIZE,
                                                  debug_mode=self.debug)

    async def on_shutdown(self):
        await self.pg_controller.on_shutdown()
        del self.pg_controller


APP_CTX = AppContext()
