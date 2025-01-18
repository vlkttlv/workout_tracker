from fastapi import HTTPException, status


class WorkoutTrackerException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class IncorrectEmailOrPasswordException(WorkoutTrackerException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"

class IncorrectTokenFormatException(WorkoutTrackerException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена проверка"

class TokenAbsentException(WorkoutTrackerException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"

class TokenExpiredException(WorkoutTrackerException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия токена истек"
    
class UserIsNotPresentException(WorkoutTrackerException):
    status_code = status.HTTP_401_UNAUTHORIZED

class UserAlreadyExistsException(WorkoutTrackerException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"

class IncorrectNumberOfExercises(WorkoutTrackerException):
    status_code = status.HTTP_409_CONFLICT
    detail = "В тренировочном плане должно быть хотя бы одно упражнение"

class IncorrectIDOfExercise(WorkoutTrackerException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Некорректный номер id упражнения"
