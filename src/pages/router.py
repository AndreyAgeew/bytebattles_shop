from fastapi import Request, APIRouter, Depends, Response, HTTPException

from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import create_access_token
from auth.dao import UserDAO
from auth.dependecies import get_current_user
from auth.models import User
from auth.router import pwd_context
from auth.schemas import SUserAuth, UserCreate
from cart.dependecies import get_current_cart
from cart.shopping_cart import ShoppingCart
from database import get_async_session
from goods.dependecies import get_active_goods
from goods.models import Goods
from order.dependecies import get_current_orders
from order.models import Order

router = APIRouter(
    prefix="/pages",
    tags=["Pages"],
)

templates = Jinja2Templates(directory="src/templates")


@router.get("/base")
def get_base_page(request: Request, user: User = Depends(get_current_user)):
    title = "Базовая страница"
    return templates.TemplateResponse(
        "base.html", {"request": request, "title": title, "user": user}
    )


@router.get("/goods")
def get_goods_page(
    request: Request,
    goods: Goods = Depends(get_active_goods),
    user: User = Depends(get_current_user),
    cart: ShoppingCart = Depends(get_current_cart),
):
    title = "Каталог"
    return templates.TemplateResponse(
        "goods.html",
        {
            "request": request,
            "title": title,
            "goods": goods,
            "user": user,
            "cart": cart,
        },
    )


@router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(response: Response, user_data: SUserAuth):
    email_or_phone = user_data.email_or_phone
    if "@" in email_or_phone:
        user = await UserDAO.one_or_none(email=email_or_phone)
    else:
        user = await UserDAO.one_or_none(phone_number=email_or_phone)
    if not user:
        raise HTTPException(404, "User not found")

    # Check if the entered password matches the hashed password from the database
    if not pwd_context.verify(user_data.password, user.hashed_password):
        raise HTTPException(401, "Incorrect password")
    jwt_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("goods_access_token", jwt_token, httponly=True)

    return {"access_token": jwt_token, "token_type": "bearer"}


@router.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
async def register_user(
    user_data: UserCreate, session: AsyncSession = Depends(get_async_session)
):
    try:
        await UserDAO.create_user(session, user_data.dict())
        return {"status": "success", "message": "User registered successfully"}
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/cart")
async def view_cart(
    request: Request,
    user: User = Depends(get_current_user),
    cart: ShoppingCart = Depends(get_current_cart),
):
    cart_items = [
        {"name": item.name, "price": item.price, "id": item.id} for item in cart
    ]
    total_price = await cart.get_total_price()
    return templates.TemplateResponse(
        "cart.html",
        {
            "request": request,
            "cart_items": cart_items,
            "total_price": total_price,
            "user": user,
        },
    )


@router.get("/orders")
async def view_orders(
    request: Request,
    user: User = Depends(get_current_user),
    orders: Order = Depends(get_current_orders),
):
    return templates.TemplateResponse(
        "orders.html", {"request": request, "orders": orders, "user": user}
    )
