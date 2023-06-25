import typing as tp

import pytest
import httpx


@pytest.fixture(scope="session")
async def async_client() -> tp.AsyncGenerator[httpx.AsyncClient, None]:
    from src.main import api_v1 as app

    async with httpx.AsyncClient(app=app, base_url="http://127.0.0.1:8000/", follow_redirects=True) as ac:
        yield ac



