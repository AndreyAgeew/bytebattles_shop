from datetime import datetime

from fastapi import Request, HTTPException, Depends
from jose import jwt, JWTError

from auth.dao import UserDAO
from config import JWT_KEY, ALGORITHM_JWT


def get_token(request: Request):
    token = request.cookies.get("goods_access_token")
    if not token:
        raise HTTPException(status_code=401)
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, JWT_KEY, ALGORITHM_JWT
        )
    except JWTError:
        raise HTTPException(status_code=401)
    expire: str = payload.get("exp")
    if not expire or int(expire) < datetime.utcnow():
        raise HTTPException(status_code=401)
    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401)
    user = await UserDAO.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401)
    return user
