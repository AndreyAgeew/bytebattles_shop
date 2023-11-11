from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("email_or_phone,password,status_code",
                         [
                             ("user@example.com", "Userpassword1!", 200),  # Корректные данные
                             ("moderator@example.com", "Moderatorpassword1", 401),  # Неверный пароль
                             ("+7333333333", "Moderatorpassword1", 404),  # Неверный логин
                         ])
async def test_login_user(email_or_phone, password, status_code, ac: AsyncClient):
    responese = await ac.post("/auth/login", json={
        "email_or_phone": email_or_phone,
        "password": password
    })
    assert responese.status_code == status_code
