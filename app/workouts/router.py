from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends

from app.exceptions import IncorrectNumberOfExercises
from app.exercises.schemas import WorkoutExercise
from app.exercises.dao import WorkoutExerciseDAO
from app.users.dependencies import get_current_user
from app.workouts.dao import WorkoutPlansDAO
from app.workouts.helper import check_correct_exercise_id
from app.workouts.schemas import AddWorkoutPlan, WorkoutPlanFull

router = APIRouter(prefix="/workout_plan", tags=["Workout plans"])

@router.post("/", status_code=201)
async def add_workout_plan(plan: AddWorkoutPlan, exercises: List[WorkoutExercise], current_user = Depends(get_current_user)):
    if exercises == []:
        raise IncorrectNumberOfExercises
    await check_correct_exercise_id(exercises)
    workout_id = await WorkoutPlansDAO.add(user_id=current_user.id, name=plan.name,
                                                   description=plan.description,
                                                   created_at=datetime.now())
    for exerc in exercises:
        await WorkoutExerciseDAO.add(workout_plan_id=workout_id,
                                    exercise_id=exerc.exercise_id, reps=exerc.reps,
                                    sets=exerc.sets, weight=exerc.weight)
    return {"status": "success", "id new workout plan": workout_id}


@router.get('/')
async def get_workout_plans(current_user = Depends(get_current_user)) -> List[WorkoutPlanFull]:
    res = await WorkoutPlansDAO.find_all(user_id = current_user.id) 
    return res
