from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from src.context import APP_CTX
from .models import User
from .manager import UserManager


async def get_user_db(session: AsyncSession = Depends(APP_CTX.pg_controller.get_async_session)):
    """Set up an alchemy session associated with user table """
    yield SQLAlchemyUserDatabase(session, user_table=User)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
