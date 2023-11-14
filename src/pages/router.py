from fastapi import Request, APIRouter, Depends, Response, HTTPException
from fastapi.responses import RedirectResponse

from fastapi.templating import Jinja2Templates

from auth.base_config import create_access_token
from auth.dao import UserDAO
from auth.dependecies import get_current_user
from auth.models import User
from auth.router import pwd_context
from auth.schemas import SUserAuth
from cart.dependecies import get_current_cart
from cart.shopping_cart import ShoppingCart
from goods.dependecies import get_active_goods
from goods.models import Goods

router = APIRouter(
    prefix="/pages",
    tags=["Pages"],
)

templates = Jinja2Templates(directory="src/templates")


@router.get("/base")
def get_base_page(request: Request, user: User = Depends(get_current_user)):
    title = "Базовая страница"
    return templates.TemplateResponse("base.html", {"request": request, "title": title, "user": user})


@router.get("/goods")
def get_goods_page(request: Request, goods: Goods = Depends(get_active_goods),
                   user: User = Depends(get_current_user)):
    title = "Каталог"
    return templates.TemplateResponse("goods.html", {"request": request, "title": title, "goods": goods, "user": user})


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
    response.set_cookie('goods_access_token', jwt_token, httponly=True)

    return {"access_token": jwt_token, "token_type": "bearer"}


@router.get("/cart")
async def view_cart(request: Request, cart: ShoppingCart = Depends(get_current_cart)):
    cart_items = [{"name": item.name, "price": item.price, "id": item.id} for item in cart]
    total_price = await cart.get_total_price()
    return templates.TemplateResponse("cart.html",
                                      {"request": request, "cart_items": cart_items, "total_price": total_price})
