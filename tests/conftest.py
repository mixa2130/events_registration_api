import os
from typing import AsyncGenerator

import asyncio
import pytest
import httpx
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import insert

from src.context import APP_CTX
from src.auth.manager import UserManager
from src.auth.utils import get_user_manager
from src.auth.models import User
from src.auth.config import current_user

load_dotenv()

DATABASE_URL_TEST = os.getenv('TESTS_PG_URI')
TEST_USER = None

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_factory = async_sessionmaker(engine_test, expire_on_commit=False)
APP_CTX.sa_metadata.bind = engine_test
APP_CTX.pg_controller.async_session_factory = async_session_factory


async def add_user():
    session: AsyncSession = async_session_factory()
    # Call async generator
    manager: UserManager = await get_user_manager().__anext__()

    new_user = {'email': os.getenv("TEST_USER_EMAIL"),
                'hashed_password': manager.password_helper.hash(os.getenv("TEST_USER_PASSWORD")),
                'is_active': True,
                'is_superuser': False,
                'is_verified': True}

    async with session.begin():
        stmt = insert(User).values(new_user).returning(User.id)
        cr_user_id = await session.execute(stmt)
        print(f"Test user created with uid {str(cr_user_id.one()[0])}")

    global TEST_USER
    TEST_USER = User(**new_user)


@pytest.fixture(scope='function')
async def session():
    async with async_session_factory() as session:
        yield session


@pytest.fixture(scope='session')
def get_test_user():
    yield TEST_USER


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(APP_CTX.sa_metadata.create_all)

    await add_user()
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(APP_CTX.sa_metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def authorized_async_client(get_test_user) -> AsyncGenerator[httpx.AsyncClient, None]:
    from src.main import api_v1 as app

    app.dependency_overrides[current_user] = lambda: get_test_user

    async with httpx.AsyncClient(app=app, base_url="http://127.0.0.1:8000/", follow_redirects=True) as ac:
        yield ac


pytest_plugins = [
    'tests.fixtures.fixture_user_auth'
]
