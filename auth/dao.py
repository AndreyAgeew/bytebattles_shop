from sqlalchemy import select

from auth.database import async_session_maker
from models.models import User


class UserDAO:
    @classmethod
    async def find_all(cls):
        async with async_session_maker() as session:
            query = select(User)
            users = await session.execute(query)
            return users.scalars().all()

    @classmethod
    async def one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(User).filter_by(**filter_by)
            user = await session.execute(query)
            return user.scalar_one_or_none()
