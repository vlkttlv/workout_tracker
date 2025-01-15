from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Exercise(Base):

    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String)
    category = Column(String)
    muscle_group = Column(String)
