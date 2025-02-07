from sqlalchemy import update, and_
from app.dao.base import BaseDAO
from app.exercises.models import Exercise, WorkoutExercise
from app.db.database import async_session_maker

class ExerciseDAO(BaseDAO):

    model = Exercise


class WorkoutExerciseDAO(BaseDAO):

    model = WorkoutExercise

    @classmethod
    async def update(cls, workout_plan_id: int, exercise_id: int, **data):
        """
        Обновляет запись

        -Аргументы:
            id: ID записи, которую надо обновить
            **data: атрибуты модели в качестве ключей и их значения в качестве значений.
        -Пример:
            await WorkoutPlansDAO.update_workout_plan(workout_id=workout_id, description=update_workout.description)
        """
        async with async_session_maker() as session:
            stmt = update(cls.model).where(and_(cls.model.exercise_id == exercise_id, cls.model.workout_plan_id == workout_plan_id)).values(**data)
            await session.execute(stmt)
            await session.commit()
