from sqlalchemy import insert
from app.dao.base import BaseDAO
from app.exercises.models import Exercise, WorkoutExercise
from app.db.database import async_session_maker

class ExerciseDAO(BaseDAO):

    model = Exercise


class WorkoutExerciseDAO(BaseDAO):

    model = WorkoutExercise

