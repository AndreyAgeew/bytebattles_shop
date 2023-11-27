from fastapi import Request, APIRouter, Depends, Response, HTTPException
from fastapi.responses import RedirectResponse

from fastapi.templating import Jinja2Templates

from src.auth.base_config import create_access_token
from src.auth.dao import UserDAO
from src.auth.dependecies import get_current_user
from src.auth.models import User
from src.auth.router import pwd_context
from src.auth.schemas import SUserAuth
from src.goods.dependecies import get_active_goods
from src.goods.models import Goods

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
def get_goods_page(request: Request, goods: Goods = Depends((get_active_goods)),
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
