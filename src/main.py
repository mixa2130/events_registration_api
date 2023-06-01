from fastapi import FastAPI

from .context import APP_CTX
from .auth.config import auth_backend, fastapi_users
from .auth.schemas import UserRead, UserCreate

app = FastAPI(
    title="Basic App"
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)


@app.on_event('startup')
async def startup_event():
    await APP_CTX.on_startup()


@app.on_event('shutdown')
async def shutdown_event():
    await APP_CTX.on_shutdown()
                                                                                                             