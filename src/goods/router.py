from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependecies import get_current_user, get_current_admin_user
from auth.models import User
from database import get_async_session
from goods.models import Goods
from goods.schemas import GoodsCreate

router = APIRouter(
    prefix="/goods",
    tags=["goods"],
)


@router.get("/")
async def get_activity_goods(user: User = Depends(get_current_user),
                             session: AsyncSession = Depends(get_async_session)):
    query = select(Goods.name).where(Goods.is_active == True)
    result = await session.execute(query)
    return [row[0] for row in result]


@router.post("/")
async def add_goods(goods_data: GoodsCreate, user: User = Depends(get_current_admin_user),
                    session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Goods).values(**goods_data.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
