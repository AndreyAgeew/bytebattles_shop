import pytest
from auth.dao import UserDAO
from database import async_session_maker


@pytest.mark.asyncio
async def test_find_all_users():
    users = await UserDAO.find_all()
    assert len(users) == 4  # 4 пользователя (3 из фикстуры и 1 из успешной регистрации в test_register_user)


@pytest.mark.asyncio
async def test_find_user_by_id():
    user_id = 1
    user = await UserDAO.find_by_id(user_id)
    assert user.email == "user@example.com"  # Первый создается обычный пользователь из data.py


@pytest.mark.asyncio
async def test_find_user_role_name():
    user_id = 1
    role_name = await UserDAO.find_user_role_name(user_id)
    assert role_name == 'user'  # Первый создается обычный пользователь из data.py


@pytest.mark.asyncio
async def test_add_users_and_find_all():
    users_data = {"email": "test1@example.com", 'name': "Test", "surname": "Testovich",
                  "phone_number": "+71234567890", "hashed_password": "Testovich123!", "role_id": 3}
    async with async_session_maker() as session:
        await UserDAO.add_all_users(session, users_data)
        users = await UserDAO.find_all()
        assert len(users) == 5  # Предполагается, что добавлен один пользователь


@pytest.mark.asyncio
async def test_add_roles_and_find_user_role_name():
    roles_data = {"name": "new"}
    async with async_session_maker() as session:
        await UserDAO.add_all_roles(session, roles_data)
        # Пользовтаель 5 созданный test_add_users_and_find_all имеет role_id 3 - admin
        user_id = 5
        role_name = await UserDAO.find_user_role_name(user_id)
        assert role_name == "admin"


@pytest.mark.asyncio
async def test_clear_user_table():
    async with async_session_maker() as session:
        await UserDAO.clear_user_table(session)
        await session.commit()
    users = await UserDAO.find_all()
    assert len(users) == 0  # Предполагается, что все пользователи удалены
