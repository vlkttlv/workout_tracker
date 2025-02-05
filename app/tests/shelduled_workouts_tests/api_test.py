"""httpx предоставляет асинхронного клиента для тестов"""
from httpx import AsyncClient
import pytest

@pytest.mark.asyncio(scope="session")
async def test_get_shelduled_workouts(auth_ac: AsyncClient):
    response = await auth_ac.get("/shelduled_workouts/", params={'status': 'pending',
                                                                 'order_by_time': 'asc'})
    assert response.status_code == 200
    assert len(response.json()) == 2
    response = await auth_ac.get("/shelduled_workouts/1")
    assert response.status_code == 200


@pytest.mark.asyncio(scope="session")
@pytest.mark.parametrize("workout_plan_id,shelduled_date,shelduled_time,status_code",
                         [(1, '2025-02-07', '18:00', 201),
                          (4, '2025-02-07', '18:00', 409)])
async def test_add_shelduled_workouts(auth_ac: AsyncClient, workout_plan_id,
                                      shelduled_date,shelduled_time,status_code):
    response = await auth_ac.post("/shelduled_workouts/", json={'workout_plan_id': workout_plan_id,
                                                                 'shelduled_date': shelduled_date,
                                                                 'shelduled_time': shelduled_time})
    assert response.status_code == status_code


@pytest.mark.asyncio(scope="session")
async def test_update_shelduled_workouts(auth_ac: AsyncClient):
    response = await auth_ac.patch("/shelduled_workouts/7", json={'shelduled_date': '2024-02-28'})
    assert response.status_code == 200
    response = await auth_ac.patch("/shelduled_workouts/7/status", params={'status': 'skip'})
    assert response.status_code == 200
    response = await auth_ac.get("/shelduled_workouts/7")
    assert response.json()['shelduled_date'] == '2024-02-28'
    assert response.json()['status'] == 'skip'
