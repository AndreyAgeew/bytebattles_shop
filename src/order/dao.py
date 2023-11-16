from sqlalchemy import select, insert, update, delete, text, desc
from sqlalchemy.exc import NoResultFound

from order.models import Order


class OrderDAO:
    @classmethod
    async def find_all(cls, session):
        query = select(Order)
        orders = await session.execute(query)
        return orders.scalars().all()

    @classmethod
    async def find_by_id(cls, session, order_id):
        query = select(Order).filter_by(id=order_id)
        result_proxy = await session.execute(query)
        order = result_proxy.scalar_one_or_none()
        if order is None:
            raise NoResultFound(f"Заказ с id={order_id} не найден")
        return order

    @classmethod
    async def add_order(cls, session, order_data):
        stmt = insert(Order).values(**order_data)
        await session.execute(stmt)

    @classmethod
    async def get_last_order_id(cls, session):
        query = select(Order.id).order_by(desc(Order.id)).limit(1)
        result_proxy = await session.execute(query)
        last_order_id = result_proxy.scalar_one_or_none()
        return last_order_id
