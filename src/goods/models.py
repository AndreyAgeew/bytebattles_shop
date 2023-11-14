from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

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
    """
    __tablename__ = "goods"

    id = Column(Integer, primary_key=True, doc="Уникальный идентификатор товара.")
    name = Column(String, nullable=False, doc="Название товара")
    price = Column(DECIMAL, nullable=False, doc="Цена за единицу товара")
    quantity = Column(Integer, nullable=False, doc="Количество доступного товара")
    updated_at = Column(TIMESTAMP, default=datetime.utcnow(), doc="Метка времени обновления товара")
    is_active = Column(Boolean, default=True, doc="Признак допуска на продажу товара")
    image_url = Column(String, nullable=True, doc="URL изображения товара")

    def __eq__(self, other):
        return isinstance(other, Goods) and self.id == other.id

    def __str__(self):
        return self.name
