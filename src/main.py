from datetime import datetime

import stripe
from fastapi import Depends, FastAPI, Header, Request
from sqladmin import Admin
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from admin.models import GoodsAdmin, UserAdmin
from auth.base_config import fastapi_users
from auth.router import router as login
from auth.schemas import UserCreate, UserRead
from cart.router import router as cart
from config import STRIPE_WEBHOOK_SECRET
from database import engine, get_async_session
from goods.dao import GoodsDAO
from goods.router import router as goods
from images.router import router as images
from order.dao import OrderDAO
from order.router import router as order
from pages.router import router as pages

app = FastAPI()
admin = Admin(app, engine)

admin.add_view(UserAdmin)
admin.add_view(GoodsAdmin)

app.mount("/static", StaticFiles(directory="src/static"), name="static")
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
        games = [
            await GoodsDAO.find_by_id(session=session, goods_id=item["id"])
            for item in order.basket_history
        ]
        for game in games:
            game.quantity -= 1
            game.updated_at = datetime.utcnow()
        order.status = 1
        await session.commit()
        print("checkout session completed")

    return {"status": "success"}
