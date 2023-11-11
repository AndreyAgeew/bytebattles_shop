import asyncio
import pytest

from auth.dao import UserDAO
from commands.data import goods_data, roles_data, users_data
from goods.dao import GoodsDAO
from main import app as fastapi_app
from src.database import async_session_maker, get_async_session

from httpx import AsyncClient


@pytest.fixture(scope="session", autouse=True)
async def prepare_data_base():
    async for session in get_async_session():
        await GoodsDAO.clear_goods_table(session)
        await session.commit()
        await UserDAO.clear_role_table(session)
        await session.commit()
        await UserDAO.clear_user_table(session)
        await session.commit()

    async with async_session_maker() as session:
        for role, user in zip(roles_data, users_data):
            await UserDAO.add_all_roles(session, role)
            await UserDAO.add_all_users(session, user)
        for goods in goods_data:
            await GoodsDAO.add_all_goods(session, goods)
        await session.commit()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function')
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope='session')
async def autheniticated_ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post("/auth/login", json={
            "email_or_phone": "user@example.com",
            "password": "Userpassword1!"
        })
        assert ac.cookies["goods_access_token"]
        yield ac
