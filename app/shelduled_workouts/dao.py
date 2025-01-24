from sqlalchemy import select, update, desc
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

    @classmethod
    async def find_all(cls, asc_or_desc: str, **filter_by):
        """
        Находит и возвращает несколько записей из таблицы БД, соответствующие условиям

        -Аргументы:
            **filter_by: атрибуты модели в качестве ключей и их значения в качестве значений.
        -Пример: 
            await Users.find_all(name='John', age=30)
            Вернет все записи, где name равно 'John' и age равно 30.
        -Возвращает:
            List[cls.model]: Список экземпляров модели, удовлетворяющих условиям фильтрации. 
            Если записи не найдены, возвращается пустой список.
        """
        async with async_session_maker() as session:
            if asc_or_desc == 'asc':
                stmt = select(cls.model).filter_by(**filter_by).order_by(
                    cls.model.shelduled_date, cls.model.shelduled_time)
            else:
                stmt = select(cls.model).filter_by(**filter_by).order_by(
                    cls.model.shelduled_date.desc(), cls.model.shelduled_time.desc())
            res = await session.execute(stmt)
            return res.scalars().all()
