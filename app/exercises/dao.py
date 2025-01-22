from sqlalchemy import update
from app.dao.base import BaseDAO
from app.exercises.models import Exercise, WorkoutExercise
from app.db.database import async_session_maker

class ExerciseDAO(BaseDAO):

    model = Exercise

    @classmethod
    async def update_exercise(cls, exercise_id: int, **data):
        """
        Обновляет запись

        -Аргументы:
            exercise_id: ID упражнения, которое надо обновить
            **data: атрибуты модели в качестве ключей и их значения в качестве значений.
        """
        async with async_session_maker() as session:
            stmt = update(cls.model).where(cls.model.id==exercise_id).values(**data)
            await session.execute(stmt)
            await session.commit()


class WorkoutExerciseDAO(BaseDAO):

    model = WorkoutExercise

    @classmethod
    async def update_exercise(cls, exercise_id: int, **data):
        """
        Обновляет запись

        -Аргументы:
            exercise_id: ID упражнения, которое надо обновить
            **data: атрибуты модели в качестве ключей и их значения в качестве значений.
        """
        async with async_session_maker() as session:
            stmt = update(cls.model).where(cls.model.exercise_id==exercise_id).values(**data)
            await session.execute(stmt)
            await session.commit()
