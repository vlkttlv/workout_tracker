"""httpx предоставляет асинхронного клиента для тестов"""
from httpx import AsyncClient
import pytest

@pytest.mark.asyncio(scope="session")
@pytest.mark.parametrize("email,password,name,status_code", [
    ("vvb63@tpu.ru", "password", "test_user", 409),
    ("example@gmail.com", "qwerty", "test_user", 422),
    ("example@gmail.com", "password", "test_user", 201),
    ("ne_email", "password", "test_user", 422)])
async def test_register_user(ac: AsyncClient, email, name,
                             password, status_code):
    """Тест, проверяющий регистрацию пользователя"""
    response = await ac.post("/auth/register", json={
        "email": email,
        "name": name,
        "password": password,
    })
    assert response.status_code == status_code

@pytest.mark.asyncio(scope="session")
@pytest.mark.parametrize("email,password,status_code", [
    ("test@test.ru", "password", 200),
    ("test@test.com", "wrong_test", 401),
    ("fake@test.com", "password", 401)
])
async def test_login_user(ac: AsyncClient, email, password, status_code):
    """Тест, проверяющий вход пользователя в систему"""
    response = await ac.post("/auth/login", json={
        "email": email,
        "password": password,
    })
    assert response.status_code == status_code
    