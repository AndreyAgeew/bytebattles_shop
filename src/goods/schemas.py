from datetime import datetime

from _decimal import Decimal
from pydantic import BaseModel


class GoodsCreate(BaseModel):
    id: int
    name: str
    price: Decimal
    quantity: int
    updated_at: datetime
    is_active: bool


class GoodsUpdate(BaseModel):
    name: str
    price: Decimal
    quantity: int
    updated_at: datetime
    is_active: bool
