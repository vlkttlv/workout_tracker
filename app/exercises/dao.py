from app.dao.base import BaseDAO
from app.exercises.models import Exercise, WorkoutExercise

class ExerciseDAO(BaseDAO):

    model = Exercise


class WorkoutExerciseDAO(BaseDAO):

    model = WorkoutExercise

