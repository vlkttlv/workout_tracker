from typing import List
from sqlalchemy import select, update, desc
from app.dao.base import BaseDAO
from app.shelduled_workouts.models import ShelduledWorkout
from app.db.database import async_session_maker


class ShelduledWorkoutDAO(BaseDAO):

    model = ShelduledWorkout

    @classmethod
    async def find_all(cls, asc_or_desc: str, **filter_by) -> List[ShelduledWorkout]:
        """
        Находит и возвращает несколько записей из таблицы БД, соответствующие условиям
        """
        async with async_session_maker() as session:
            if asc_or_desc == "asc":
                stmt = (
                    select(cls.model)
                    .filter_by(**filter_by)
                    .order_by(cls.model.shelduled_date, cls.model.shelduled_time)
                )
            else:
                stmt = (
                    select(cls.model)
                    .filter_by(**filter_by)
                    .order_by(
                        cls.model.shelduled_date.desc(), cls.model.shelduled_time.desc()
                    )
                )
            res = await session.execute(stmt)
            return res.scalars().all()
