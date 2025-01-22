from typing import List
from fastapi import APIRouter, Depends
from app.exceptions import IncorrectIDOfExercise, IncorrectRoleOfUser
from app.exercises.dao import ExerciseDAO
from app.exercises.schemas import Exercise, AddExercise, UpdateExercise
from app.users.dependencies import get_current_user

router = APIRouter(prefix="/exercises", tags=["Exercises"])


@router.get("/", summary="Returns all the exercises")
async def get_all_exercises() -> List[Exercise]:
    """Возвращает все упражнения"""
    result = await ExerciseDAO.find_all()
    return result

@router.get("/{exercise_id}", summary="Returns a specific exercise")
async def get_exercise(exercise_id: int):
    """Находит и возвращает конкретное упражнение """
    result = await ExerciseDAO.find_one_or_none(id=exercise_id)
    if result is None:
        raise IncorrectIDOfExercise
    return result

@router.post("/", summary="Adds a new exercise")
async def add_exercise(exercise: AddExercise, current_user = Depends(get_current_user)):
    """
    Добавляет новое упражнение в БД
    Доступно только администраторам
    """
    if current_user.role != "admin":
        raise IncorrectRoleOfUser
    exrc_id = await ExerciseDAO.add(name=exercise.name,
                                    category=exercise.category, muscle_group=exercise.muscle_group)
    return {"status": "success", "details": f"Было добавлено упражнение с ID = {exrc_id}"}

@router.delete("/{exercise_id}", summary="Deletes the exercise")
async def delete_exercise(exercise_id: int, current_user = Depends(get_current_user)):
    """
    Добавляет конкретное упражнение
    Доступно только администраторам
    """
    if current_user.role != "admin":
        raise IncorrectRoleOfUser
    current_exerc = await ExerciseDAO.find_one_or_none(id=exercise_id)
    if current_exerc is None:
        raise IncorrectIDOfExercise
    await ExerciseDAO.delete(id=exercise_id)
    return {"status": "success", "details": f"Было удалено упражнение с ID = {exercise_id}"}

@router.patch("/{exercise_id}", summary="Updates the exercise")
async def patch_exercise(exercise_id: int, exercise: UpdateExercise, current_user = Depends(get_current_user)):
    """
    Изменяет упражнение
    Доступно только администраторам
    """
    if current_user.role != "admin":
        raise IncorrectRoleOfUser
    current_exerc = await ExerciseDAO.find_one_or_none(id=exercise_id)
    if current_exerc is None:
        raise IncorrectIDOfExercise
    if exercise.name is not None:
        await ExerciseDAO.update_exercise(exercise_id=exercise_id, name=exercise.name)
    if exercise.category is not None:
        await ExerciseDAO.update_exercise(exercise_id=exercise_id, category=exercise.category)
    if exercise.muscle_group is not None:
        await ExerciseDAO.update_exercise(exercise_id=exercise_id, muscle_group=exercise.muscle_group)
    return {"status": "success"}
