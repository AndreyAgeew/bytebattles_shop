from datetime import datetime

import stripe
import uvicorn
from fastapi import Depends, FastAPI, Header, Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from prometheus_fastapi_instrumentator import Instrumentator
from redis import asyncio as aioredis
from sqladmin import Admin
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from src.admin.models import GoodsAdmin, UserAdmin
from src.auth.base_config import fastapi_users
from src.auth.dao import UserDAO
from src.auth.router import router as login
from src.auth.schemas import UserCreate, UserRead
from src.cart.router import router as cart
from src.config import BASE_DIR, REDIS_HOST, REDIS_PORT, STRIPE_WEBHOOK_SECRET
from src.database import engine, get_async_session
from src.goods.dao import GoodsDAO
from src.goods.router import router as goods
from src.images.router import router as images
from src.jobs.tasks import send_order_confirmation_email
from src.order.dao import OrderDAO
from src.order.router import router as order
from src.pages.router import router as pages

app = FastAPI()
admin = Admin(app, engine)

admin.add_view(UserAdmin)
admin.add_view(GoodsAdmin)

app.mount("/static", StaticFiles(directory=f"{BASE_DIR}/static"), name="static")
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")


instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)

Instrumentator().instrument(app).expose(app)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(login)
app.include_router(goods)
app.include_router(pages)
app.include_router(images)
app.include_router(cart)
app.include_router(order)


@app.post("/webhook")
async def webhook_received(
        request: Request,
        stripe_signature: str = Header(None),
        session: AsyncSession = Depends(get_async_session),
):
    webhook_secret = STRIPE_WEBHOOK_SECRET
    data = await request.body()
    try:
        event = stripe.Webhook.construct_event(
            payload=data, sig_header=stripe_signature, secret=webhook_secret
        )
        event_data = event["data"]
    except Exception as e:
        return {"error": str(e)}
    order_id = await OrderDAO.get_last_order_id(session=session)
    event_type = event["type"]
    if event_type == "product.created":
        print("product.created")
    elif event_type == "checkout.session.completed":
        order = await OrderDAO.find_by_id(session=session, order_id=order_id)
        user = await UserDAO.find_by_id(order.initiator_id)
        games = [
            await GoodsDAO.find_by_id(session=session, goods_id=item["id"])
            for item in order.basket_history
        ]
        order_dict = {'id': order.id,
                      'created_at': order.created_at,
                      'games': [game.name for game in games]}
        for game in games:
            game.quantity -= 1
            game.updated_at = datetime.utcnow()
        order.status = 1
        await session.commit()
        send_order_confirmation_email.delay(user.email, order_dict)
        print("checkout session completed")

    return {"status": "success"}


if __name__ == "__main__":
    uvicorn.run("src.main:app", reload=True)
