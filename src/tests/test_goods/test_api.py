import pytest
from httpx import AsyncClient


# Тест проверяет, что получение списка товаров без аутентификации возвращает статус код 401 (Unauthorized).
@pytest.mark.asyncio
async def test_get_activity_goods_not_login(ac: AsyncClient):
    response = await ac.get("/goods/")
    assert response.status_code == 401


# Тест проверяет, что получение списка товаров с аутентификацией возвращает статус код 200 (OK).
@pytest.mark.asyncio
async def test_get_activity_goods_in_login(autheniticated_user_ac: AsyncClient):
    response = await autheniticated_user_ac.get("/goods/")
    assert response.status_code == 200


# Тест проверяет, что получение информации о товаре без аутентификации возвращает статус код 401 (Unauthorized).
@pytest.mark.asyncio
async def test_get_goods_not_login(ac: AsyncClient):
    response = await ac.get("/goods/1")
    assert response.status_code == 401


# Тест проверяет, что получение информации о товаре с аутентификацией возвращает статус код 200 (OK)
# и правильный идентификатор товара.
@pytest.mark.asyncio
async def test_get_goods_in_login(autheniticated_user_ac: AsyncClient):
    response = await autheniticated_user_ac.get("/goods/1")
    assert response.status_code == 200
    assert response.json().get('id') == 1


# Тест проверяет, что попытка добавления товара пользователем возвращает статус код 403 (Forbidden).
@pytest.mark.asyncio
async def test_add_goods_user_login(autheniticated_user_ac: AsyncClient):
    goods_data = {"id": 8, "name": "Test Goods", "price": 1000, "quantity": 50, "updated_at": "2023-11-12T11:04:51.724",
                  "is_active": True}
    response = await autheniticated_user_ac.post("/goods/", json=goods_data)

    assert response.status_code == 403


# Тест проверяет, что попытка добавления товара модератором возвращает статус код 403 (Forbidden).
@pytest.mark.asyncio
async def test_add_goods_moderator_login(autheniticated_moderator_ac: AsyncClient):
    goods_data = {"id": 8, "name": "Test Goods", "price": 1000, "quantity": 50, "updated_at": "2023-11-12T11:04:51.724",
                  "is_active": True}
    response = await autheniticated_moderator_ac.post("/goods/", json=goods_data)

    assert response.status_code == 403


# Тест проверяет, что успешное добавление товара администратором возвращает статус код 201 (Created)
# и "success" в ответе.
@pytest.mark.asyncio
async def test_add_goods_admin_login(autheniticated_admin_ac: AsyncClient):
    goods_data = {"id": 8, "name": "Test Goods", "price": 1000, "quantity": 50, "updated_at": "2023-11-12T11:04:51.724",
                  "is_active": True}
    response = await autheniticated_admin_ac.post("/goods/", json=goods_data)

    assert response.status_code == 201
    assert response.json()["status"] == "success"


# Тест проверяет, что попытка обновления товара модератором возвращает статус код 200 (OK) и "success" в ответе.
@pytest.mark.asyncio
async def test_update_goods_moderator_login(autheniticated_moderator_ac: AsyncClient):
    goods_data = {"id": 1, "name": "Test1 Goods", "price": 1000, "quantity": 50,
                  "updated_at": "2023-11-12T11:04:51.724",
                  "is_active": True}
    response = await autheniticated_moderator_ac.put("/goods/1", json=goods_data)

    assert response.status_code == 200
    assert response.json()["status"] == "success"


# Тест проверяет, что попытка удаления товара модератором возвращает статус код 403 (Forbidden).
@pytest.mark.asyncio
async def test_delete_goods_moderator_login(autheniticated_moderator_ac: AsyncClient):
    response = await autheniticated_moderator_ac.delete("/goods/1")

    assert response.status_code == 403


# Тест проверяет, что успешное удаление товара администратором возвращает статус код 200 (OK) и "success" в ответе.
@pytest.mark.asyncio
async def test_delete_goods_admin_login(autheniticated_admin_ac: AsyncClient):
    response = await autheniticated_admin_ac.delete("/goods/1")

    assert response.status_code == 200
    assert response.json()["status"] == "success"
