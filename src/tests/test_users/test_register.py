from httpx import AsyncClient
import pytest


@pytest.mark.parametrize(
    "user_params, status_code",
    [
        ({
             "email": "test@example.com",
             "password": "Testovich123!",
             "confirm_password": "Testovich123!",
             "name": "Test",
             "surname": "Testenovich",
             "patronymic": None,
             "phone_number": "+79999999999",
             "role_id": 1
         }, 201),  # Ожидаем успешную регистрацию без ошибок
        ({
             "email": "test@example.com",
             "password": "Testovich123!",
             "confirm_password": "InvalidPassword",  # Не совпадает с паролем
             "name": "Test",
             "surname": "Testenovich",
             "patronymic": None,
             "phone_number": "+79999999999",
             "role_id": 1
         }, 400),  # Ожидаем ошибку валидации пароля
        ({
             "email": "test@example.com",
             "password": "Testovich123!",
             "confirm_password": "Testovich123!",
             "name": "Test",
             "surname": "Testenovich",
             "patronymic": None,
             "phone_number": "+799999999999",  # Некорректный номер телефона
             "role_id": 1
         }, 400),  # Ожидаем ошибку валидации телефона
        ({
             "email": "testexample.com",  # Некорректный email
             "password": "Testovich123!",
             "confirm_password": "Testovich123!",
             "name": "Test",
             "surname": "Testenovich",
             "patronymic": None,
             "phone_number": "+79999999999",
             "role_id": 1
         }, 422),  # Ожидаем ошибку валидации email
    ]
)
async def test_register_user(ac: AsyncClient, user_params, status_code):
    response = await ac.post("/auth/register", json=user_params)

    assert response.status_code == status_code
