from pydantic import BaseModel, Field



class Exercise(BaseModel):

    id: int
    name: str
    category: str
    muscle_group: str


class WorkoutExercise(BaseModel):


    exercise_id: int = Field(gt = 5)
    reps: int = Field(gt = 0)
    sets: int = Field(gt = 0)
    weight: int = Field(gt = 0)
