from typing import List
from fastapi import APIRouter
from app.exercises.dao import ExerciseDAO
from app.exercises.schemas import Exercise

router = APIRouter(prefix="/exercises", tags=["Exercises"])

@router.get("/")
async def get_all_exercises() -> List[Exercise]:
    result = await ExerciseDAO.find_all()
    return result

@router.get("/{exercise_id}")
async def get_exercise(exercise_id: int) -> Exercise:
    result = await ExerciseDAO.find_one_or_none(id=exercise_id)
    return result