from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependecies import get_current_user
from auth.models import User
from database import get_async_session
from goods.dao import GoodsDAO
from goods.shopping_cart import ShoppingCart


async def get_active_goods(session: AsyncSession = Depends(get_async_session)):
    goods = await GoodsDAO.find_active(session)
    return goods


# Глобальный словарь для хранения связи между пользователем и его корзиной
user_carts = {}


async def get_current_cart(user: User = Depends(get_current_user)):
    if user.id not in user_carts:
        user_carts[user.id] = ShoppingCart()
    return user_carts[user.id]
