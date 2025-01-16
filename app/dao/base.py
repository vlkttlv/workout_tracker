from sqlalchemy import delete, insert, select
from app.db.database import async_session_maker

class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        """
        Находит и возвращает одну запись из таблицы в БД

        -Аргументы:
            **filter_by: атрибуты модели в качестве ключей и их значения в качестве значений.
        -Возвращает:
            Optional[cls.model]: Экземпляр модели, если запись найдена.
            Если запись не найдена, возвращается None.
        """
        async with async_session_maker() as session:
            stmt = select(cls.model).filter_by(**filter_by)
            res = await session.execute(stmt)
            # вернёт либо одно значение, либо None, если записей не найдено
            return res.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
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
            stmt = select(cls.model).filter_by(**filter_by)
            res = await session.execute(stmt)
            return res.scalars().all()

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
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def delete(cls, **filter_by):
        """
        Удаляет запись из таблицы БД по соотвествующему условию

        -Аргументы:
        **filter_by: атрибуты модели в качестве ключей и их значения в качестве значений.
        -Пример: 
            await MyModel.delete(name='Alice') - Это удалит все записи, где name равно 'Alice'.
        """
        async with async_session_maker() as session:
            stmt = delete(cls.model).filter_by(**filter_by)
            await session.execut(stmt)
            await session.commit()
            