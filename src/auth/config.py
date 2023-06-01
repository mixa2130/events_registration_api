import uuid

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

# from auth.manager import get_user_manager
from .models import User
from .utils import get_user_manager
from src.context import APP_CTX


cookie_transport = CookieTransport(cookie_name="RGcookie", cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=APP_CTX.JWT_SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
