from datetime import datetime, timedelta

import jwt
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)

from src.auth.manager import get_user_manager
from src.auth.models import User
from src.config import ALGORITHM_JWT, JTWTS_KEY, JWT_KEY

cookie_transport = CookieTransport(cookie_max_age=3600)

JTWTS_KEY = JTWTS_KEY


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=JTWTS_KEY, lifetime_seconds=3600)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_KEY, ALGORITHM_JWT)
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
