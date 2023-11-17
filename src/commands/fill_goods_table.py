import os
import sys
import asyncio
import click

current_file = os.path.abspath(__file__)

BASE_DIR = os.path.dirname(os.path.dirname(current_file))

sys.path.insert(0, BASE_DIR)
from commands.data import goods_data, roles_data, users_data
from database import get_async_session
from order.dao import OrderDAO
from goods.dao import GoodsDAO
from auth.dao import UserDAO

src_dir = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.append(src_dir)


async def main():
    try:
        async for session in get_async_session():
            await GoodsDAO.clear_goods_table(session)
            await session.commit()
            await OrderDAO.clear_order_table(session)
            await session.commit()
            await UserDAO.clear_role_table(session)
            await session.commit()
            await UserDAO.clear_user_table(session)
            await session.commit()

            for role, user in zip(roles_data, users_data):
                await UserDAO.add_all_roles(session, role)
                await UserDAO.add_all_users(session, user)
            for goods in goods_data:
                await GoodsDAO.add_all_goods(session, goods)
            await session.commit()
            click.echo("Таблицы успешно заполнены.")

    except Exception as e:
        click.echo(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    asyncio.run(main())
