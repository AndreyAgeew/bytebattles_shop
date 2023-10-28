from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Role(Base):
    """
    Модель данных для ролей в SQLAlchemy.

    Атрибуты:
        id (Column): Уникальный идентификатор роли.
        name (Column): Название роли.
        permissions (Column): JSON-объект, содержащий ролевые разрешения.
    """
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, doc="Уникальный идентификатор роли.")
    name = Column(String, nullable=False, doc="Название роли.")
    permissions = Column(JSON, doc="JSON-объект, содержащий ролевые разрешения.")


class User(Base):
    """
    Модель данных для пользователей в SQLAlchemy.

    Атрибуты:
        id (Column): Уникальный идентификатор пользователя.
        name (Column): Имя пользователя.
        surname (Column): Фамилия пользователя.
        patronymic (Column): Отчество пользователя (по желанию).
        phone_number (Column): Номер телефона пользователя.
        password (Column): Хэш пароля пользователя.
        registered_at (Column): Метка времени регистрации пользователя.
        role_id (Column): Идентификатор связанной с пользователем роли.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, doc="Уникальный идентификатор пользователя.")
    name = Column(String, nullable=False, doc="Имя пользователя.")
    surname = Column(String, nullable=False, doc="Фамилия пользователя.")
    patronymic = Column(String, nullable=True, doc="Отчество пользователя (по желанию).")
    phone_number = Column(String, nullable=False, doc="Номер телефона пользователя.")
    password = Column(String, nullable=False, doc="Хэш пароля пользователя.")
    registered_at = Column(TIMESTAMP, default=datetime.utcnow(), doc="Метка времени регистрации пользователя.")
    role_id = Column(Integer, ForeignKey('roles.id', ondelete='CASCADE'),
                     doc="Идентификатор связанной с пользователем роли.")
