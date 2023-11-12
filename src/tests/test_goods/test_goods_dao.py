from datetime import datetime

import pytest

from goods.dao import GoodsDAO
from database import async_session_maker


@pytest.mark.asyncio
async def test_find_all_goods():
    async with async_session_maker() as session:
        goods = await GoodsDAO.find_all(session)
        assert len(goods) == 7  # 7 товаров (из фикстуры)


@pytest.mark.asyncio
async def test_find_active_goods():
    async with async_session_maker() as session:
        goods = await GoodsDAO.find_active(session)

    assert all(good.is_active for good in goods)  # Все товары активны


@pytest.mark.asyncio
async def test_find_goods_by_id():
    goods_id = 2
    async with async_session_maker() as session:
        goods = await GoodsDAO.find_by_id(session, goods_id)

    # Второй созданный товар из фикстуры (первый может удалится в проверках роутера)
    assert goods.name == "DARK SOULS 4"


@pytest.mark.asyncio
async def test_add_goods_and_find_all():
    goods_data = {
        "id": 9,
        "name": "New Goods",
        "price": 1000,
        "quantity": 50,
        "updated_at": datetime(2023, 11, 12, 11, 4, 51, 724),
        "is_active": True
    }
    async with async_session_maker() as session:
        await GoodsDAO.add_goods(session, goods_data)
        goods = await GoodsDAO.find_all(session)

    assert len(goods) == 8  # Предполагается, что добавлен один товар


@pytest.mark.asyncio
async def test_update_goods_and_find_by_id():
    goods_id = 2
    updated_data = {"name": "Updated Product", "price": 25.0}
    async with async_session_maker() as session:
        await GoodsDAO.update_goods(session, goods_id, updated_data)
        goods_id = 2
        updated_good = await GoodsDAO.find_by_id(session, goods_id)
        assert updated_good.name == "Updated Product"  # Проверяем, что товар обновлен


@pytest.mark.asyncio
async def test_delete_goods():
    goods_id = 2
    async with async_session_maker() as session:
        await GoodsDAO.delete_goods(session, goods_id)
        goods = await GoodsDAO.find_all(session)
        assert len(goods) == 6  # Проверяем, что товар удален и их стало на один меньше


@pytest.mark.asyncio
async def test_update_goods_image():
    goods_id = 3
    image_url = "/src/test/img/test.jpg"
    async with async_session_maker() as session:
        await GoodsDAO.update_goods_image(session, goods_id, image_url)
        updated_good = await GoodsDAO.find_by_id(session, goods_id)
        assert updated_good.image_url == image_url  # Проверяем, что изображение товара обновлено


@pytest.mark.asyncio
async def test_clear_goods_table():
    async with async_session_maker() as session:
        await GoodsDAO.clear_goods_table(session)
        goods = await GoodsDAO.find_all(session)
        assert len(goods) == 0  # Предполагается, что все товары удалены из таблицы
