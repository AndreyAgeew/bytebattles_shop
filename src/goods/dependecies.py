from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.goods.dao import GoodsDAO


async def get_active_goods(session: AsyncSession = Depends(get_async_session)):
    goods = await GoodsDAO.find_active(session)
    return goods
