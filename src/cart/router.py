from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from cart.dependecies import get_current_cart
from cart.shopping_cart import ShoppingCart
from database import get_async_session
from goods.dao import GoodsDAO

router = APIRouter(
    prefix="/cart",
    tags=["cart"],
)


@router.get("/add_to_cart/{goods_id}")
async def add_to_cart(
    goods_id: int,
    session: AsyncSession = Depends(get_async_session),
    cart: ShoppingCart = Depends(get_current_cart),
):
    item = await GoodsDAO.find_by_id(session, goods_id)
    if item:
        await cart.add_item(item)

    return {"status": "success"}


@router.get("/remove_to_cart/{goods_id}")
async def remove_to_cart(
    goods_id: int,
    session: AsyncSession = Depends(get_async_session),
    cart: ShoppingCart = Depends(get_current_cart),
):
    item = await GoodsDAO.find_by_id(session, goods_id)
    if item:
        await cart.remove_item(item)

    return {"status": "success"}


@router.get("/view_cart")
async def view_cart(cart: ShoppingCart = Depends(get_current_cart)):
    cart_items = [{"name": item.name, "price": item.price} for item in cart]
    total_price = await cart.get_total_price()
    return {"cart_items": cart_items, "total_price": total_price}
