from typing import List
from pydantic import BaseModel

from app.exercises.schemas import Exercise, WorkoutExercise


class AddWorkoutPlan(BaseModel):

    name: str
    description: str

class WorkoutPlanFull(BaseModel):
    workout_plan_id: int
    user_id: int
    name: str
    description: str
    exercises: List[WorkoutExercise]
