from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE_URL
else:
    DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(DATABASE_URL)  # движок

# генератор сессий; expire_on_commit - завершение транзакций
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):  # для миграций, здесь аккумулируются все данные
    pass
