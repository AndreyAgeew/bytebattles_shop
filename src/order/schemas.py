from datetime import datetime

from pydantic import BaseModel


class OrderCreate(BaseModel):
    initiator_id: int
    basket_history: dict
