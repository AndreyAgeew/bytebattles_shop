from datetime import datetime

import stripe
from sqlalchemy import DECIMAL, TIMESTAMP, Boolean, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Goods(Base):
    """
    Модель товара в базе данных.

    Атрибуты:
        id (Column): Уникальный идентификатор товара.
        name (Column): Название товара.
        price (Column): Цена за единицу товара.
        quantity (Column): Количество доступного товара.
        updated_at (Column): Метка времени обновления товара.
        is_active (Column): Признак допуска на продажу товара.
        image_url (Column): URL изображения товара

    Методы:
         __eq__:  Сравнивает текущий объект Goods с другим объектом Goods.
         __str__:  Возвращает строковое представление объекта Goods.
         create_stripe_product_price:  Создает продукт и цену в системе платежей Stripe.
    """

    __tablename__ = "goods"

    id = Column(Integer, primary_key=True, doc="Уникальный идентификатор товара.")
    name = Column(String, nullable=False, unique=True, doc="Название товара")
    price = Column(DECIMAL, nullable=False, doc="Цена за единицу товара")
    quantity = Column(Integer, nullable=False, doc="Количество доступного товара")
    updated_at = Column(
        TIMESTAMP, default=datetime.utcnow(), doc="Метка времени обновления товара"
    )
    is_active = Column(Boolean, default=True, doc="Признак допуска на продажу товара")
    image_url = Column(String, nullable=True, doc="URL изображения товара")

    def __eq__(self, other):
        """
        Сравнивает текущий объект Goods с другим объектом Goods.

        Параметры:
            other (Goods): Другой объект Goods.

        Возвращает:
            bool: True, если объекты равны, иначе False.
        """
        return isinstance(other, Goods) and self.id == other.id

    def __str__(self):
        """
        Возвращает строковое представление объекта Goods.

        Возвращает:
            str: Строковое представление объекта Goods.
        """
        return self.name

    def create_stripe_product_price(self):
        """
        Создает продукт и цену в системе платежей Stripe.

        Возвращает:
            dict: Информация о созданной цене в системе Stripe.
        """
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product["id"], unit_amount=self.price * 100, currency="rub"
        )
        return stripe_product_price
