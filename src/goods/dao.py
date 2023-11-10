from sqlalchemy import select, insert, update, delete

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
        goods = await session.execute(query)
        return goods.scalar_one_or_none()

    @classmethod
    async def add_goods(cls, session, goods_data):
        stmt = insert(Goods).values(**goods_data)
        await session.execute(stmt)

    @classmethod
    async def add_all_goods(cls, session, goods_data):
        try:
            goods = Goods(**goods_data)
            async with session.begin():
                session.add(goods)
            await session.commit()
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    @classmethod
    async def update_goods(cls, session, goods_id, goods_data):
        stmt = update(Goods).where(Goods.id == goods_id).values(**goods_data)
        await session.execute(stmt)

    @classmethod
    async def delete_goods(cls, session, goods_id):
        stmt = delete(Goods).where(Goods.id == goods_id)
        await session.execute(stmt)

    @classmethod
    async def update_goods_image(cls, session, goods_id, image_url):
        stmt = update(Goods).where(Goods.id == goods_id).values(image_url=image_url)
        await session.execute(stmt)
