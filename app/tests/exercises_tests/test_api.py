"""httpx предоставляет асинхронного клиента для тестов"""

from httpx import AsyncClient
import pytest


@pytest.mark.asyncio(scope="session")
async def test_get_all_exercises(ac: AsyncClient, status_code=200):
    response = await ac.get("/exercises/")
    assert response.status_code == status_code
    assert len(response.json()) == 14


@pytest.mark.asyncio(scope="session")
@pytest.mark.parametrize("status_code,exercise_id", [(200, 1), (409, 20)])
async def test_get_exercise(ac: AsyncClient, status_code, exercise_id):
    response = await ac.get(f"/exercises/{exercise_id}")
    assert response.status_code == status_code


@pytest.mark.asyncio(scope="session")
async def test_add_exercise(auth_ac: AsyncClient):
    response = await auth_ac.post(
        "/exercises/",
        json={"name": "string", "category": "string", "muscle_group": "string"},
    )
    assert response.status_code == 201
    assert response.json()["details"] == "Было добавлено упражнение с ID = 15"

    response = await auth_ac.post(
        "/exercises/", json={"name": "string", "category": "string"}
    )
    assert response.status_code == 422


@pytest.mark.asyncio(scope="session")
async def test_delete_exercise(auth_ac: AsyncClient):
    response = await auth_ac.delete("/exercises/15")
    assert response.status_code == 200
    assert response.json()["details"] == "Было удалено упражнение с ID = 15"

    response = await auth_ac.get("/exercises/")
    assert len(response.json()) == 14
