from fastapi import Depends

from src.auth.dependecies import get_current_user
from src.auth.models import User
from src.cart.shopping_cart import ShoppingCart

# Глобальный словарь для хранения связи между пользователем и его корзиной
user_carts = {}


async def get_current_cart(user: User = Depends(get_current_user)):
    if user.id not in user_carts:
        user_carts[user.id] = ShoppingCart()
    return user_carts[user.id]
