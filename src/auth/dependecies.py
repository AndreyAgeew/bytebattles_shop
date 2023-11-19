from datetime import datetime

from fastapi import Request, HTTPException, Depends
import jwt
from auth.dao import UserDAO
from auth.models import User
from config import JWT_KEY, ALGORITHM_JWT


def get_token(request: Request):
    path = request.url.path
    token = request.cookies.get("goods_access_token")
    if not token:
        # Если токен отсутствует, делаем перенаправление для сайта
        if path.startswith("/pages"):
            redirect_url = "/pages/login"
            raise HTTPException(status_code=307, detail=f"Redirect to {redirect_url}",
                                headers={"Location": redirect_url})
        else:
            raise HTTPException(status_code=401, detail="Access token is missing. You are not authenticated.")
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, JWT_KEY, ALGORITHM_JWT)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired. Please re-authenticate.")
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Token decoding error. Please re-authenticate.")
    expire = payload.get("exp")
    if not expire or int(expire) < datetime.utcnow().timestamp():
        raise HTTPException(status_code=401, detail="Token has expired. Please re-authenticate.")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="User identifier is missing in the token. Please re-authenticate.")
    user = await UserDAO.find_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="User with the specified identifier not found.")
    return user


async def get_current_admin_user(current_user: User = Depends(get_current_user)):
    role_name = await UserDAO.find_user_role_name(current_user.id)
    if role_name != 'admin':
        raise HTTPException(status_code=403, detail="You do not have sufficient permissions to perform this operation.")
    return current_user


async def get_current_moderator_or_admin_user(current_user: User = Depends(get_current_user)):
    role_name = await UserDAO.find_user_role_name(current_user.id)
    if role_name == 'user':
        raise HTTPException(status_code=403, detail="You do not have sufficient permissions to perform this operation.")
    return current_user
