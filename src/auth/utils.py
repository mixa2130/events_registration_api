from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy.sql as sa

from src.context import APP_CTX
from .models import User, RoleTbl
from .manager import UserManager
from .exceptions import DatabaseNotReady


async def get_user_db(session: AsyncSession = Depends(APP_CTX.pg_controller.get_async_session)):
    """Set up an alchemy session associated with user table """
    yield SQLAlchemyUserDatabase(session, user_table=User)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


async def get_basic_user_role_id(session: AsyncSession) -> int:
    stmt = sa.select(RoleTbl.c.id).where(RoleTbl.c.name == 'user')
    _res = await session.execute(stmt)
    role_id = _res.one()
    if role_id is None:
        raise DatabaseNotReady
    return role_id[0]
