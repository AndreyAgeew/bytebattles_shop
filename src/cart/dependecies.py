from fastapi import Depends

from auth.dependecies import get_current_user
from auth.models import User
from cart.shopping_cart import ShoppingCart

# Глобальный словарь для хранения связи между пользователем и его корзиной
user_carts = {}


async def get_current_cart(user: User = Depends(get_current_user)):
    print("Getting current cart for user:", user.id)
    if user.id not in user_carts:
        user_carts[user.id] = ShoppingCart()
    return user_carts[user.id]
