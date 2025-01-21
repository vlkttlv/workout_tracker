from app.exceptions import IncorrectIDOfExercise
from app.exercises.dao import ExerciseDAO


async def check_correct_exercise_id(exercises):
    """Проверяет, что ID упражнения не больше максимального ID в БД"""
    res =  await ExerciseDAO.find_all()
    last_id = res[-1].id
    for exerc in exercises:
        if exerc.exercise_id > last_id:
            raise IncorrectIDOfExercise
