from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from auth.dependecies import (
    get_current_user,
    get_current_admin_user,
    get_current_moderator_or_admin_user,
)
from auth.models import User
from database import get_async_session
from goods.dao import GoodsDAO
from goods.schemas import GoodsCreate, GoodsUpdate

router = APIRouter(
    prefix="/goods",
    tags=["goods"],
)


@router.get("/")
async def get_activity_goods(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    goods = await GoodsDAO.find_all(session)
    return goods


@router.get("/{goods_id}")
async def get_goods(
    user: User = Depends(get_current_user),
    goods_id: int = Path(..., title="Goods ID"),
    session: AsyncSession = Depends(get_async_session),
):
    goods = await GoodsDAO.find_by_id(session, goods_id)
    if goods is None:
        raise HTTPException(status_code=404, detail="Goods not found")
    return goods


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_goods(
    goods_data: GoodsCreate,
    user: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_async_session),
):
    await GoodsDAO.add_goods(session, goods_data.dict())
    await session.commit()
    return {"status": "success"}


@router.put("/{goods_id}")
async def update_goods(
    goods_data: GoodsUpdate,
    goods_id: int = Path(..., title="Goods ID"),
    user: User = Depends(get_current_moderator_or_admin_user),
    session: AsyncSession = Depends(get_async_session),
):
    existing_goods = await GoodsDAO.find_by_id(session, goods_id)
    if existing_goods is None:
        raise HTTPException(status_code=404, detail="Goods not found")
    await GoodsDAO.update_goods(session, goods_id, goods_data.dict())
    await session.commit()
    return {"status": "success"}


@router.delete("/{goods_id}")
async def delete_goods(
    goods_id: int = Path(..., title="Goods ID"),
    user: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_async_session),
):
    existing_goods = await GoodsDAO.find_by_id(session, goods_id)
    if existing_goods is None:
        raise HTTPException(status_code=404, detail="Goods not found")
    await GoodsDAO.delete_goods(session, goods_id)
    await session.commit()
    return {"status": "success"}
