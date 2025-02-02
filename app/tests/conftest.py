from datetime import datetime
import json
from sqlalchemy import insert
import pytest
from app.db.database import Base, async_session_maker, engine
from app.config import settings

from app.users.models import Users
from app.exercises.models import Exercise, WorkoutExercise
from app.workouts.models import WorkoutPlans
from app.shelduled_workouts.models import ShelduledWorkout

from httpx import AsyncClient

from app.main import app as fastapi_app

@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    assert settings.MODE == "TEST"
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_test_json(model: str):
        with open(f"app/tests/mock_data/test_{model}.json", "r", encoding='utf-8 ') as file:
            return json.load(file)

    users = open_test_json("users")
    exercises = open_test_json("exercises")
    workout_plans = open_test_json("workout_plans")
    workout_exercises = open_test_json("workout_exercises")
    shelduled_workouts = open_test_json("shelduled_workouts")

    for workout_plan in workout_plans:
        workout_plan["created_at"] = datetime.strptime(workout_plan["created_at"], '%Y-%m-%d %H:%M:%S')

    for shelduled_workout in shelduled_workouts:
        shelduled_workout["shelduled_date"] = datetime.strptime(shelduled_workout["shelduled_date"], '%Y-%m-%d')
        shelduled_workout["shelduled_time"] = datetime.strptime(shelduled_workout["shelduled_time"], '%H:%M:%S')


    async with async_session_maker() as session:
        add_users = insert(Users).values(users)
        add_exercises = insert(Exercise).values(exercises)
        add_workout_plans = insert(WorkoutPlans).values(workout_plans)
        add_workout_exercises = insert(WorkoutExercise).values(workout_exercises)
        add_shelduled_workouts = insert(ShelduledWorkout).values(shelduled_workouts)

        await session.execute(add_users)
        await session.execute(add_exercises)
        await session.execute(add_workout_plans)
        await session.execute(add_workout_exercises)
        await session.execute(add_shelduled_workouts)

        await session.commit()

@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def auth_ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post("auth/login", json={"email": "vvb63@tpu.ru", "password": "password"})
        assert ac.cookies["access_token"]
        yield ac


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session