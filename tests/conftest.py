import os

import asyncio
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from src.main import app
from src.context import APP_CTX

from dotenv import load_dotenv

load_dotenv()
DATABASE_URL_TEST = os.getenv('TESTS_PG_URI')

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_factory = async_sessionmaker(engine_test, expire_on_commit=False)
APP_CTX.sa_metadata.bind = engine_test
APP_CTX.pg_controller.async_session_factory = async_session_factory


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session


# app.dependency_overrides[APP_CTX.pg_controller.get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(APP_CTX.sa_metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(APP_CTX.sa_metadata.drop_all)


# SETUP
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000/api/v1", follow_redirects=True) as ac:
        yield ac
