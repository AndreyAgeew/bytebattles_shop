from datetime import datetime
from typing import AsyncGenerator

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import TIMESTAMP, Boolean, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

from src.auth.models import Role
from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

Base: DeclarativeMeta = declarative_base()


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, doc="Уникальный идентификатор пользователя."
    )
    email: Mapped[str] = mapped_column(
        String(length=320),
        unique=True,
        index=True,
        nullable=False,
        doc="Email пользователя.",
    )
    name: Mapped[str] = mapped_column(String, nullable=False, doc="Имя пользователя.")
    surname: Mapped[str] = mapped_column(
        String, nullable=False, doc="Фамилия пользователя."
    )
    patronymic: Mapped[str] = mapped_column(
        String, nullable=True, doc="Отчество пользователя (по желанию)."
    )
    phone_number: Mapped[str] = mapped_column(
        String, nullable=False, unique=True, doc="Номер телефона пользователя."
    )
    registered_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        default=datetime.utcnow(),
        doc="Метка времени регистрации пользователя.",
    )
    role_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(Role.id, ondelete="CASCADE"),
        nullable=True,
        doc="Идентификатор связанной с пользователем роли.",
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False, doc="Хэш пароля пользователя."
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False, doc="Активен ли пользователь."
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        doc="Является ли пользователь администратором.",
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, doc="Подтвержден ли пользователь."
    )


engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
