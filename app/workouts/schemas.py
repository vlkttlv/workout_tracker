from datetime import datetime
from typing import List
from pydantic import BaseModel, Field

from app.exercises.schemas import WorkoutExerciseWithoutID, WorkoutExercise


class AddWorkoutPlan(BaseModel):

    name: str
    description: str

class WorkoutPlanFull(BaseModel):
    workout_plan_id: int
    user_id: int
    name: str
    description: str
    created_at: datetime
    exercises: List[WorkoutExercise]


class UpdateWorkoutPlan(BaseModel):
    name: str = Field(default=None)
    description: str = Field(default=None)


class UpdateWorkoutExercise(BaseModel):
    exercise: WorkoutExerciseWithoutID

