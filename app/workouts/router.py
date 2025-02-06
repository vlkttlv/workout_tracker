from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, Query

from app.exceptions import IncorrectNumberOfExercises
from app.exercises.schemas import WorkoutExercise
from app.exercises.dao import WorkoutExerciseDAO
from app.users.dependencies import get_current_user
from app.workouts.dao import WorkoutPlansDAO
from app.workouts.helper import check_correct_exercise_id
from app.workouts.schemas import (AddWorkoutPlan, WorkoutPlanFull,
                                  UpdateWorkoutExercise, UpdateWorkoutPlan)

router = APIRouter(prefix="/workout_plan", tags=["Workout plans"])

@router.post("/", status_code=201, summary="Creates a new workout plan")
async def add_workout_plan(plan: AddWorkoutPlan,
                           exercises: List[WorkoutExercise],
                           current_user = Depends(get_current_user)):
    """Создает план тренировки"""
    if exercises == []:
        raise IncorrectNumberOfExercises
    await check_correct_exercise_id(exercises)

    workout_id = await WorkoutPlansDAO.add(
        user_id=current_user.id,
        name=plan.name,
        description=plan.description,
        created_at=datetime.now())
    for exerc in exercises:
        await WorkoutExerciseDAO.add(
            workout_plan_id=workout_id,
            exercise_id=exerc.exercise_id,
            reps=exerc.reps,
            sets=exerc.sets,
            weight=exerc.weight,
            user_id=current_user.id)
    return {"status": "success", "ID of the new workout plan": workout_id}


@router.get("/", summary="Returns the user's workout plans")
async def get_workout_plans(current_user = Depends(get_current_user)) -> List[WorkoutPlanFull]:
    """Находит и возвращает все планы тренировок пользователя"""
    res = await WorkoutPlansDAO.find_all(user_id = current_user.id)
    return res

@router.get("/{workout_id}", summary="Returns the user's workout plan by ID")
async def get_workout_plan(workout_id:int, current_user = Depends(get_current_user)) -> List[WorkoutPlanFull]:
    """Находит и возвращает все планы тренировок пользователя"""
    res = await WorkoutPlansDAO.find_by_id(workout_plan_id=workout_id, user_id=current_user.id)
    return res

@router.delete("/{workout_id}", summary="Deletes the workout plan")
async def delete_workout_plan(workout_id: int, current_user=Depends(get_current_user)):
    """Удаляет план тренировки по указанному ID"""
    await WorkoutExerciseDAO.delete(workout_plan_id=workout_id, user_id=current_user.id)
    await WorkoutPlansDAO.delete(id=workout_id, user_id=current_user.id)


@router.patch("/{workout_id}",
              summary="Updates the workout plan and returns the workout plan")
async def update_workout_plan(update_workout: UpdateWorkoutPlan, workout_id: int,
                              current_user=Depends(get_current_user)):
    """
    Обновляет имя и/или описание плана тренировок по указанному идентификатору.
    """
    if update_workout.name is not None:
        await WorkoutPlansDAO.update(id=workout_id, name=update_workout.name )
    if update_workout.description is not None:
        await WorkoutPlansDAO.update(id=workout_id,
                                     description=update_workout.description)
    workout_plan = await WorkoutPlansDAO.find_by_id(workout_plan_id=workout_id, user_id=current_user.id)
    return workout_plan


@router.patch("/{workout_id}/exercises/{exercise_id}",
              summary="Updates the exercise in the workout plan and returns the workout plan")
async def update_workout_exercise(workout_id: int, exercise_id: int,
                                  update_exercise: UpdateWorkoutExercise,
                                  current_user = Depends(get_current_user)):
    """    
    Обновляет параметры упражнения (количество повторений/подходов/вес)
    в плане тренировок по указанным идентификаторам.
    """
    if update_exercise.reps is not None:
        await WorkoutExerciseDAO.update(workout_id, exercise_id, reps=update_exercise.reps)
    if update_exercise.sets is not None:
        await WorkoutExerciseDAO.update(workout_id, exercise_id, sets=update_exercise.sets)
    if update_exercise.weight is not None:
        await WorkoutExerciseDAO.update(workout_id, exercise_id, 
                                         weight=update_exercise.weight)
    workout_plan = await WorkoutPlansDAO.find_by_id(workout_plan_id=workout_id, user_id=current_user.id)
    return workout_plan
