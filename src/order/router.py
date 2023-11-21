from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependecies import get_current_user
from src.auth.models import User
from src.cart.dependecies import get_current_cart
from src.database import get_async_session
from src.goods.dao import GoodsDAO

from .dao import OrderDAO
from .payment import get_stripe_session

router = APIRouter(
    prefix="/order",
    tags=["order"],
)


@router.post("/create_order")
async def create_order(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        # Получаем текущую корзину пользователя
        current_cart = await get_current_cart(user)

        # Преобразуем basket_history в JSON-совместимый формат
        basket_history_data = jsonable_encoder(current_cart.items)

        goods = [
            await GoodsDAO.find_by_id(session=session, goods_id=game["id"])
            for game in basket_history_data
        ]
        # Добавляем заказ с использованием OrderDAO
        await OrderDAO.add_order(
            session,
            {
                "initiator_id": user.id,
                "basket_history": basket_history_data,
            },
        )
        await current_cart.clear_cart()
        await session.commit()

        # Получаем ссылку на платежную сессию
        payment_url = get_stripe_session(goods=goods, user=user)
    except Exception as e:
        print(f"Error during order creation: {e}")

    # Возвращаем JSON-ответ с URL-адресом платежной сессии
    return {"message": "Order created successfully", "payment_url": payment_url}
