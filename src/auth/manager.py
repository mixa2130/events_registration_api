import uuid
from typing import Optional, Union

from fastapi import Request
from fastapi_users import BaseUserManager, UUIDIDMixin, InvalidPasswordException
from fastapi_users import schemas as fu_schemas
from fastapi_users import models as fu_models
from fastapi_users import exceptions as fu_exc

from src.context import APP_CTX
from .models import User


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = APP_CTX.JWT_SECRET
    verification_token_secret = APP_CTX.JWT_SECRET

    async def validate_password(
            self,
            password: str,
            user: Union[fu_schemas.UC, User],
    ) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(
                reason="Password should be at least 8 characters"
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason="Password should not contain e-mail"
            )

    async def create(
            self,
            user_create: fu_schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> fu_models.UP:
        await self.validate_password(user_create.password, user_create)

        # user_db works with db table users
        existing_user = await self.user_db.get_by_email(user_create.email)

        if existing_user is not None:
            raise fu_exc.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        # session = await APP_CTX.pg_controller.get_async_session().__anext__()
        # basic_role_id = await utils.get_basic_user_role_id(session)
        # user_dict["role_id"] = basic_role_id

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        APP_CTX.logger.info(f"User {user.id} has registered.")

    async def on_after_forgot_password(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")
