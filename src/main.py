from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from admin.models import UserAdmin, GoodsAdmin
from auth.base_config import fastapi_users
from auth.schemas import UserRead, UserCreate

from auth.router import router as login
from database import engine
from goods.router import router as goods
from pages.router import router as pages
from images.router import router as images
from sqladmin import Admin

from src.config import BASE_DIR

app = FastAPI()
admin = Admin(app, engine)

admin.add_view(UserAdmin)
admin.add_view(GoodsAdmin)

app.mount("/static", StaticFiles(directory=F"{BASE_DIR}/static"), name="static")
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(login)
app.include_router(goods)
app.include_router(pages)
app.include_router(images)
