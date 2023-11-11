import asyncio
import pytest

from auth.dao import UserDAO
from commands.data import goods_data, roles_data, users_data
from goods.dao import GoodsDAO
from src.database import async_session_maker, get_async_session


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
