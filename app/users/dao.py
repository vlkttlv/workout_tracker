from app.dao.base import BaseDAO
from app.users.models import RefreshToken, Users

class UsersDAO(BaseDAO):
    
    model = Users

class TokenDAO(BaseDAO):

    model = RefreshToken
    