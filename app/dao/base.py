from app.database import async_session_maker

class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(id: int):
        async with async_session_maker() as session:
            pass

    @classmethod
    async def find_all(**filter):
        async with async_session_maker() as session:
            pass

    @classmethod
    async def add(**data):
        async with async_session_maker() as session:
            pass

    @classmethod
    async def delete(**filter):
        async with async_session_maker() as session:
            pass