import os
import typing as tp

import pytest
import httpx


@pytest.fixture(scope="function")
async def jwt_authorized_async_client() -> tp.AsyncGenerator[httpx.AsyncClient, None]:
    from src.main import api_v1 as app

    async with httpx.AsyncClient(app=app,
                                 base_url=os.getenv("TEST_BASE_URL"), follow_redirects=True) as ac:
        auth_req = await ac.post('auth/jwt/login',
                                 data={'username': os.getenv("TEST_USER_EMAIL"),
                                       'password': os.getenv("TEST_USER_PASSWORD")})
        assert auth_req.status_code == 204
        yield ac


@pytest.fixture(scope="function")
async def async_client() -> tp.AsyncGenerator[httpx.AsyncClient, None]:
    from src.main import api_v1 as app

    async with httpx.AsyncClient(app=app,
                                 base_url=os.getenv("TEST_BASE_URL"), follow_redirects=True) as ac:
        yield ac
