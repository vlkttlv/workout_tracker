from fastapi import APIRouter, Depends, Response
import jwt
from jwt.exceptions import InvalidTokenError
from app.exceptions import (IncorrectEmailOrPasswordException,
                            IncorrectTokenFormatException, UserAlreadyExistsException)
from app.users.auth import (authenticate_user, create_access_token,
                            create_refresh_token, get_password_hash)
from app.users.dependencies import get_current_user, get_refresh_token
from app.users.schemas import UserRegister, UserLogin
from app.users.dao import TokenDAO, UsersDAO
from app.config import settings

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register", status_code=201)
async def register_user(user_data: UserRegister):
    """Регистрация пользователя"""
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, name=user_data.name,
                        hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_data: UserLogin):
    """Аутенфикация пользователя"""
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = await create_refresh_token(data={"sub": str(user.id)})
    response.set_cookie("access_token", access_token, httponly=True)
    return {"access_token": access_token,
            "refresh_token": refresh_token,
            "details": f"привет, {user.name}!"}

@router.post("/refresh")
async def refresh_token(response: Response, refresh_token: str = Depends(get_refresh_token)):
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, settings.ALGORITHM)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise IncorrectTokenFormatException
    except InvalidTokenError as e:
        raise IncorrectTokenFormatException from e
    new_access_token = create_access_token({"sub": user_id})
    response.set_cookie("access_token", new_access_token, httponly=True)
    return {"access_token": new_access_token}

@router.post("/logout")
async def logout_user(response: Response, current_user = Depends(get_current_user)):
    """Выход из системы"""
    response.delete_cookie("access_token")
    await TokenDAO.delete(user_id=current_user.id) # удаляем refresh токен
