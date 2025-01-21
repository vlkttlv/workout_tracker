from sqlalchemy import Column, ForeignKey, Integer, String
from app.db.database import Base

class Exercise(Base):

    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String)
    category = Column(String)
    muscle_group = Column(String)


class WorkoutExercise(Base):

    __tablename__ = "workout_exercises"

    id = Column(Integer, primary_key=True, nullable=False)
    workout_plan_id = Column(Integer, ForeignKey('workout_plans.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    exercise_id = Column(Integer, ForeignKey('exercises.id'), nullable=False)
    reps = Column(Integer, nullable=False)
    sets = Column(Integer, nullable=False)
    weight = Column(Integer)

