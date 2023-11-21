from passlib.context import CryptContext
from sqlalchemy import delete, select, text
from sqlalchemy.exc import IntegrityError

from auth.models import Role, User
from auth.validaters import validate_password, validate_phone
from database import async_session_maker

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserDAO:
    @classmethod
    async def create_user(cls, session, data):
        validate_password(data["password"], data["confirm_password"])
        validate_phone(data["phone_number"])
        user_data = {
            "name": data["name"],
            "surname": data["surname"],
            "phone_number": data["phone_number"],
            "email": data["email"],
            "hashed_password": pwd_context.hash(data["password"]),
            "role_id": 1,
            "is_active": data["is_active"],
            "is_superuser": data["is_superuser"],
            "is_verified": data["is_verified"],
        }

        user = User(**user_data)
        async with session.begin():
            try:
                session.add(user)
                await session.commit()
            except IntegrityError:
                await session.rollback()
                raise Exception("User with this email already exists.")

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

    @classmethod
    async def find_by_id(cls, user_id):
        async with async_session_maker() as session:
            query = select(User).filter_by(id=user_id)
            user = await session.execute(query)
            return user.scalar_one_or_none()

    @classmethod
    async def find_user_role_name(cls, user_id):
        async with async_session_maker() as session:
            query = select(Role.name).join(User).filter(User.id == user_id)
            result = await session.execute(query)
            role_name = result.scalar()
            return role_name

    @classmethod
    async def add_all_users(cls, session, users_data):
        users = User(**users_data)
        async with session.begin():
            session.add(users)
        await session.commit()

    @classmethod
    async def add_all_roles(cls, session, roles_data):
        roles = Role(**roles_data)
        async with session.begin():
            session.add(roles)
        await session.commit()

    @classmethod
    async def clear_user_table(cls, session):
        try:
            stmt = delete(User)
            await session.execute(stmt)
            await session.execute(text("ALTER SEQUENCE user_id_seq RESTART WITH 1"))
            print(f"Таблица User очищена!")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    @classmethod
    async def clear_role_table(cls, session):
        try:
            stmt = delete(Role)
            await session.execute(stmt)
            await session.execute(text("ALTER SEQUENCE role_id_seq RESTART WITH 1"))
            print(f"Таблица Role очищена!")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
