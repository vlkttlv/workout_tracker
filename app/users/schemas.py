from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    name: str = Field(..., min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    password: str = Field(..., min_length=8, max_length=50, description="Пароль, от 8 до 50 знаков")
    

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=8, max_length=50, description="Пароль, от 8 до 50 знаков")

class SUsers(BaseModel):
    id: int = Field(..., description="ID пользователя")
    name: str = Field(..., description="Имя пользователя")