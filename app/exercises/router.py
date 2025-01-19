from typing import List
from fastapi import APIRouter, Depends
from app.exceptions import IncorrectIDOfExercise, IncorrectRoleOfUser
from app.exercises.dao import ExerciseDAO
from app.exercises.schemas import Exercise, AddExercise, ExerciseUpdate
from app.users.dependencies import get_current_user

router = APIRouter(prefix="/exercises", tags=["Exercises"])


@router.get("/")
async def get_all_exercises() -> List[Exercise]:
    result = await ExerciseDAO.find_all()
    return result

@router.get("/{exercise_id}")
async def get_exercise(exercise_id: int):
    result = await ExerciseDAO.find_one_or_none(id=exercise_id)
    if result is None:
        raise IncorrectIDOfExercise
    return result

@router.post("/")
async def add_exercise(exercise: AddExercise, current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise IncorrectRoleOfUser
    exrc_id = await ExerciseDAO.add(name=exercise.name,
                                    category=exercise.category, muscle_group=exercise.muscle_group)
    return {"status": "success", "details": f"Было добавлено упражнение с ID = {exrc_id}"}

@router.delete("/{exercise_id}")
async def delete_exercise(exercise_id: int, current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise IncorrectRoleOfUser
    current_exerc = await ExerciseDAO.find_one_or_none(id=exercise_id)
    if current_exerc is None:
        raise IncorrectIDOfExercise
    await ExerciseDAO.delete(id=exercise_id)
    return {"status": "success", "details": f"Было удалено упражнение с ID = {exercise_id}"}

@router.patch("/{exercise_id}")
async def patch_exercise(exercise_id: int, exercise: ExerciseUpdate, current_user = Depends(get_current_user)):
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

