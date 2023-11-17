import stripe
from fastapi import FastAPI, Request, Header
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from admin.models import UserAdmin, GoodsAdmin
from auth.base_config import fastapi_users
from auth.schemas import UserRead, UserCreate

from auth.router import router as login
from config import STRIPE_WEBHOOK_SECRET
from database import engine
from goods.router import router as goods
from pages.router import router as pages
from images.router import router as images
from cart.router import router as cart
from order.router import router as order
from sqladmin import Admin

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
async def webhook_received(request: Request, stripe_signature: str = Header(None)):
    webhook_secret = STRIPE_WEBHOOK_SECRET
    data = await request.body()
    try:
        event = stripe.Webhook.construct_event(
            payload=data,
            sig_header=stripe_signature,
            secret=webhook_secret
        )
        event_data = event['data']
    except Exception as e:
        return {"error": str(e)}

    event_type = event['type']
    if event_type == 'checkout.session.completed':
        pass
    elif event_type == 'invoice.payment_failed':
        pass
    elif event_type == 'price.created':
        pass

    return {"status": "success"}
