"""httpx предоставляет асинхронного клиента для тестов"""
from httpx import AsyncClient
import pytest
from app.exercises.dao import WorkoutExerciseDAO
from app.tests.workout_plans_tests.mock_data import mock_workout_plan

@pytest.mark.asyncio(scope="session")
async def test_get_workout_plan(auth_ac: AsyncClient):
    response = await auth_ac.get("/workout_plan/")
    assert response.status_code == 200
    assert len(response.json()) == 3
    response = await auth_ac.get("/workout_plan/1")
    assert response.status_code == 200
    response = await auth_ac.get("/workout_plan/4")
    assert response.json() == []

@pytest.mark.asyncio(scope="session")
async def test_add_and_delete_workout_plan(auth_ac: AsyncClient):
    response = await auth_ac.post("/workout_plan/", json=mock_workout_plan)
    assert response.status_code == 201
    response = await auth_ac.get("/workout_plan/")
    assert response.status_code == 200
    assert len(response.json()) == 4
    response = await auth_ac.delete("/workout_plan/5")
    assert response.status_code == 200
    response = await auth_ac.get("/workout_plan/")
    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.asyncio(scope="session")
async def test_update_workout_plan(auth_ac: AsyncClient):
    response = await auth_ac.patch("/workout_plan/1", json={"name": "leg day"})
    assert response.status_code == 200
    assert response.json()[0]['name'] == 'leg day'
    response = await auth_ac.patch("/workout_plan/1/exercises/9", json={"reps": 10})
    assert response.status_code == 200
    result = await WorkoutExerciseDAO.find_one_or_none(workout_plan_id=1, exercise_id=9)
    assert result.reps == 10
