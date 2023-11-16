from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from auth.dependecies import get_current_user
from cart.dependecies import get_current_cart
from database import get_async_session
from auth.models import User
from .payment import get_stripe_session
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
    total_price = await current_cart.get_total_price()

    # Добавляем заказ с использованием OrderDAO
    await OrderDAO.add_order(session, {
        'initiator_id': user.id,
        'basket_history': basket_history_data,
    })
    await current_cart.clear_cart()
    await session.commit()

    # Получаем ID последнего добавленного заказа
    last_order_id = await OrderDAO.get_last_order_id(session)

    # Получаем ссылку на платежную сессию
    payment_url = get_stripe_session(order_id=last_order_id,
                                     amount=total_price,
                                     user=user)

    # Возвращаем JSON-ответ с URL-адресом платежной сессии
    return {"message": "Order created successfully", "payment_url": payment_url}
