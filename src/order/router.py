from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from auth.dependecies import get_current_user
from cart.dependecies import get_current_cart
from database import get_async_session
from auth.models import User
from .schemas import OrderCreate
from .dao import OrderDAO

router = APIRouter(
    prefix="/order",
    tags=["order"],
)


@router.post("/create_order")
async def create_order(order_data: OrderCreate,
                       user: User = Depends(get_current_user),
                       session: AsyncSession = Depends(get_async_session)):
    # Получаем текущую корзину пользователя
    current_cart = await get_current_cart(user)

    # Преобразуем basket_history в JSON-совместимый формат
    basket_history_data = jsonable_encoder(current_cart.items)

    # Добавляем заказ с использованием OrderDAO
    await OrderDAO.add_order(session, {
        'initiator_id': user.id,
        'basket_history': basket_history_data,
    })
    await current_cart.clear_cart()
    await session.commit()
    return {"message": "Order created successfully"}
