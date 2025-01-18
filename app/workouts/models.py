from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.db.database import Base

class WorkoutPlans(Base):

    __tablename__ = "workout_plans"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String)
    description = Column(String)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    
