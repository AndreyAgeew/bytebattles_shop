from fastapi import APIRouter, Response, HTTPException
from passlib.context import CryptContext

from src.auth.base_config import create_access_token
from src.auth.dao import UserDAO
from src.auth.schemas import SUserAuth

# Create an instance of the password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


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


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie('goods_access_token')
