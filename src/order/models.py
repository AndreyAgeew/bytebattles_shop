from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from auth.models import User

Base = declarative_base()


class Order(Base):
    """
    Модель данных для заказов в SQLAlchemy.

    Атрибуты:
        id (Column): Уникальный идентификатор заказа.
        initiator_id (Column): Идентификатор пользователя-инициатора заказа.
        basket_history (Column): История корзины заказа.
        created_at (Column): Метка времени создания заказа.
        status (Column): Статус заказа.
    """

    __tablename__ = "order"

    CREATED = 0
    PAID = 1
    CANCELED = 2
    STATUSES = {
        CREATED: "Создан",
        PAID: "Оплачен",
        CANCELED: "Отменен",
    }

    id = Column(Integer, primary_key=True, doc="Уникальный идентификатор заказа.")
    initiator_id = Column(
        Integer,
        ForeignKey(User.id, ondelete="SET NULL"),
        nullable=False,
        doc="Идентификатор пользователя-инициатора заказа.",
    )
    basket_history = Column(JSON, doc="История корзины заказа.")
    created_at = Column(
        TIMESTAMP, default=datetime.utcnow, doc="Метка времени создания заказа."
    )
    status = Column(Integer, default=CREATED, doc="Статус заказа.")
