from datetime import datetime, timedelta

import jwt
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend

from fastapi_users.authentication import JWTStrategy

from auth.manager import get_user_manager
from auth.models import User
from config import JTWTS_KEY

cookie_transport = CookieTransport(cookie_max_age=3600)

JTWTS_KEY = JTWTS_KEY


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=JTWTS_KEY, lifetime_seconds=3600)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, "asdlajsdasASDASD", "HS256"
    )
    return encoded_jwt


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
