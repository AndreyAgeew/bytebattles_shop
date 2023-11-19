from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependecies import get_current_user
from auth.models import User
from database import get_async_session
from order.dao import OrderDAO


async def get_current_orders(session: AsyncSession = Depends(get_async_session),
                             user: User = Depends(get_current_user)):
    orders = await OrderDAO.find_all(session)
    user_orders = [order for order in orders if order.initiator_id == user.id]
    return user_orders
