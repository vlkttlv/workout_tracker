from sqlalchemy import update
from app.dao.base import BaseDAO
from app.shelduled_workouts.models import ShelduledWorkout
from app.db.database import async_session_maker

class ShelduledWorkoutDAO(BaseDAO):

    model = ShelduledWorkout

    @classmethod
    async def update(cls, shelduled_workout_id: int, **data):
        """
        Обновляет запись

        -Аргументы:
            shelduled_workout_id: ID тренировки, которую надо обновить
        """
        async with async_session_maker() as session:
            stmt = update(cls.model).where(cls.model.id==shelduled_workout_id).values(**data)
            await session.execute(stmt)
            await session.commit()
