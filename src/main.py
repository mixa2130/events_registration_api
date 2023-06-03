from fastapi import FastAPI

from .context import APP_CTX
from .auth.config import auth_backend, fastapi_users
from .auth.schemas import UserRead, UserCreate
from .events.router import router as events_router

app = FastAPI(
    title="Basic App"
)

api_v1 = FastAPI()

api_v1.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

api_v1.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

api_v1.include_router(events_router)

app.mount("/api/v1", api_v1)


@app.on_event('startup')
async def startup_event():
    await APP_CTX.on_startup()


@app.on_event('shutdown')
async def shutdown_event():
    await APP_CTX.on_shutdown()
