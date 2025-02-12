from datetime import date, time

from sqlalchemy import Column, Date, ForeignKey, Integer, String, Time
from app.db.database import Base


class ShelduledWorkout(Base):

    __tablename__ = "shelduled_workout"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    workout_plan_id = Column(Integer, ForeignKey("workout_plans.id"), nullable=False)
    shelduled_date = Column(Date, nullable=False, default=date)
    shelduled_time = Column(Time, nullable=False, default=time)
    status = Column(String, nullable=False, default="pending")
