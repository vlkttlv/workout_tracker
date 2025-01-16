from datetime import datetime, timedelta
import jwt
from pydantic import EmailStr
from passlib.context import CryptContext
from app.users.dao import TokenDAO, UsersDAO
from app.exceptions import IncorrectEmailOrPasswordException
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

def get_password_hash(password: str) -> str:
    """Генерирует хэшированный пароль"""
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    """
    Проверяет пароль на валидность

    -Аргументы:
        plain_password: пароль пользователя в обычном виде
        hashed_password: захэшированный пароль"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """Создает access токен"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)


async def create_refresh_token(data: dict) -> str:
    """Создает refresh токен"""
    to_encode = data.copy()
    now_time = datetime.utcnow()
    expire = now_time + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    user_id = int(data["sub"])
    token_user = await TokenDAO.find_one_or_none(user_id=user_id)
    if not token_user:
        await TokenDAO.add(token=token, user_id=user_id, created_at=now_time, expires_at=expire)
    else:
        await TokenDAO.update_token( created_at=now_time, expires_at=expire, user_id=user_id, token=token)
    return token

async def authenticate_user(email: EmailStr, password: str):
    """Аутенфицирует пользователя
    
    Проверяет, есть ли пользователь с такой почтой в БД и совпадает ли введенный пароль
    
    -Возвращает:
        Optional[users]: Экземпляр модели пользователя, если запись найдена.
        Если запись не найдена, возвращается None."""
    user = await UsersDAO.find_one_or_none(email=email)
    if not (user and verify_password(password, user.hashed_password)):
        raise IncorrectEmailOrPasswordException
    return user
