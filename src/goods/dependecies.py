from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from goods.dao import GoodsDAO
from goods.shopping_cart import ShoppingCart


async def get_active_goods(session: AsyncSession = Depends(get_async_session)):
    goods = await GoodsDAO.find_active(session)
    return goods


async def get_current_cart():
    cart = ShoppingCart()
    return cart
