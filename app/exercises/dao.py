from app.dao.base import BaseDAO
from app.exercises.models import Exercise


class ExerciseDAO(BaseDAO):

    model = Exercise