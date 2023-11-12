from sqlalchemy import select, insert, update, delete, text
from sqlalchemy.exc import NoResultFound

from goods.models import Goods


class GoodsDAO:
    @classmethod
    async def find_all(cls, session):
        query = select(Goods)
        goods = await session.execute(query)
        return goods.scalars().all()

    @classmethod
    async def find_active(cls, session):
        query = select(Goods).filter_by(is_active=True)
        goods = await session.execute(query)
        return goods.scalars().all()

    @classmethod
    async def find_by_id(cls, session, goods_id):

        query = select(Goods).filter_by(id=goods_id)
        result_proxy = await session.execute(query)
        goods = result_proxy.scalar_one_or_none()
        if goods is None:
            raise NoResultFound(f"Товар с id={goods_id} не найден")

        return goods

    @classmethod
    async def add_goods(cls, session, goods_data):
        stmt = insert(Goods).values(**goods_data)
        await session.execute(stmt)

    @classmethod
    async def add_all_goods(cls, session, goods_data):
        goods = Goods(**goods_data)
        async with session.begin():
            session.add(goods)
        await session.commit()

    @classmethod
    async def update_goods(cls, session, goods_id, goods_data):
        goods = await cls.find_by_id(session, goods_id=goods_id)
        stmt = update(Goods).where(Goods.id == goods.id).values(**goods_data)
        await session.execute(stmt)

    @classmethod
    async def delete_goods(cls, session, goods_id):
        goods = await cls.find_by_id(session, goods_id=goods_id)
        stmt = delete(Goods).where(Goods.id == goods.id)
        await session.execute(stmt)

    @classmethod
    async def update_goods_image(cls, session, goods_id, image_url):
        goods = cls.find_by_id(session, goods_id=goods_id)
        stmt = update(Goods).where(Goods.id == goods_id).values(image_url=image_url)
        await session.execute(stmt)

    @classmethod
    async def clear_goods_table(cls, session):
        try:
            stmt = delete(Goods)
            await session.execute(stmt)
            await session.execute(text("ALTER SEQUENCE goods_id_seq RESTART WITH 1"))
            print(f"Таблица Goods очищена!")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
