from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime

from app.db.database import Base


class Users(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    

class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'
    token = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False) 
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
