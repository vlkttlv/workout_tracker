from sqlalchemy import update
from app.dao.base import BaseDAO
from app.users.models import RefreshToken, Users
from app.db.database import async_session_maker
class UsersDAO(BaseDAO):
    
    model = Users

class TokenDAO(BaseDAO):

    model = RefreshToken

    @classmethod
    async def update_token(cls, user_id: int, token):
        async with async_session_maker() as session:
            stmt = update(cls.model).where(user_id==user_id).values(token=token)
            await session.execute(stmt)
            await session.commit()
