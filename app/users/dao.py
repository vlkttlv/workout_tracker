from sqlalchemy import insert, update
from app.dao.base import BaseDAO
from app.users.models import RefreshToken, Users
from app.db.database import async_session_maker
class UsersDAO(BaseDAO):
    
    model = Users

class TokenDAO(BaseDAO):

    model = RefreshToken

    @classmethod
    async def add(cls, **data):
        """
        Добавляет запись в таблицу БД

        -Аргументы:
            **data: атрибуты модели в качестве ключей и их значения в качестве значений.
        -Пример: 
            await Users.add(name='Alice', age=25)
            Это добавит новую запись с именем 'Alice' и возрастом 25.
        """
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**data)
            res = await session.execute(stmt)
            await session.commit()

    @classmethod
    async def update_token(cls, created_at, expires_at, user_id: int):
        """
        Обновляет refresh токен в БД

        -Аргументы:
            created_at: время создания токена
            expires_at: время истечения жизни токена
            user_id: индетификатор пользователя
            token: токен
        """
        async with async_session_maker() as session:
            stmt = update(cls.model).where(user_id==user_id).values(created_at=created_at, expires_at=expires_at)
            await session.execute(stmt)
            await session.commit()
