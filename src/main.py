from fastapi import FastAPI

from auth.base_config import fastapi_users
from auth.schemas import UserRead, UserCreate

from auth.router import router as login

app = FastAPI()


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(login)
