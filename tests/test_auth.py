import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from src.auth.models import User

new_user = {
    "email": "test_user@example.com",
    "password": "I'm_new_user_mf",
    "is_active": True,
    "is_superuser": False,
    "is_verified": False
}


async def test_jwt_register(async_client: httpx.AsyncClient, session: AsyncSession):
    response = await async_client.post("/auth/jwt/register", json=new_user)
    assert response.status_code == 201

    stmt = select(User).where(User.email == new_user['email'])
    _res = await session.execute(stmt)
    _res.one()


async def test_jwt_login(async_client: httpx.AsyncClient, session: AsyncSession):
    login_data = {'username': new_user['email'],
                  'password': new_user['password']
                  }
    response = await async_client.post("/auth/jwt/login", data=login_data)
    assert response.status_code == 204


async def test_jwt_login_not_superuser(async_client: httpx.AsyncClient, session: AsyncSession):
    login_data = {'username': new_user['email'],
                  'password': new_user['password'],
                  'is_superuser': True
                  }
    response = await async_client.post("/auth/jwt/login", data=login_data)
    assert response.status_code == 204

    stmt = select(User).where(User.email == new_user['email'])
    _res = await session.execute(stmt)
    user = _res.one()[0]
    assert user.is_superuser is False


async def test_jwt_logout(async_client: httpx.AsyncClient):
    response = await async_client.post("/auth/jwt/logout")
    assert response.status_code == 401

    login_data = {'username': new_user['email'],
                  'password': new_user['password']
                  }
    response = await async_client.post("/auth/jwt/login", data=login_data)
    assert response.status_code == 204

    response = await async_client.post("/auth/jwt/logout")
    assert response.status_code == 204
