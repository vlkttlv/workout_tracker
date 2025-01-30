import asyncio
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
# фикстура - функция, котор-я подготавливает среду для тестирования


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    assert settings.MODE == "TEST"
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_test_json(model: str):
        with open(f"app/tests/test_{model}.json", "r", encoding='utf-8 ') as file:
            return json.load(file)

    # hotels = open_test_json("hotels")
    # rooms = open_test_json("rooms")
    users = open_test_json("users")
    exercises = open_test_json("exercises")
    # bookings = open_test_json("bookings")
    # payments = open_test_json("payments")

    # for booking in bookings:
    #     booking["date_from"] = datetime.strptime(
    #         booking["date_from"], "%Y-%m-%d")
    #     booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")

    # for payment in payments:
    #     payment["date_to"] = datetime.strptime(payment["date_to"], "%Y-%m-%d")

    async with async_session_maker() as session:
        add_users = insert(Users).values(users)
        add_exercises = insert(Exercise).values(exercises)

        await session.execute(add_users)
        await session.execute(add_exercises)

        await session.commit()

@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def auth_ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post("auth/login", json={"email": "test@test.com", "password": "password"})
        assert ac.cookies["access_token"]
        yield ac


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session