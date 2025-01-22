from pydantic import BaseModel, Field



class Exercise(BaseModel):

    id: int
    name: str
    category: str
    muscle_group: str

class AddExercise(BaseModel):

    name: str = Field(min_length=3)
    category: str = Field(min_length=3)
    muscle_group: str = Field(min_length=3)

class UpdateExercise(BaseModel):
    name: str = Field(default=None, title="Name of the exercise")
    category: str = Field(default=None, title="Category of the exercise")
    muscle_group: str = Field(default=None, title="Muscle group targeted by the exercise")


class WorkoutExercise(BaseModel):
    exercise_id: int = Field(gt = 5)
    reps: int = Field(gt = 0)
    sets: int = Field(gt = 0)
    weight: int = Field(gt = 0)

class WorkoutExerciseWithoutID(BaseModel):
    reps: int = Field(gt = 0)
    sets: int = Field(gt = 0)
    weight: int = Field(gt = 0)

