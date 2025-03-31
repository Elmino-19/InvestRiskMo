from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.sql import func
from src.config.database import Base

class UserAssessment(Base):
    __tablename__ = "user_assessments"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    step = Column(String)
    numeric_answers = Column(JSON)
    text_answers = Column(JSON)
    total_score = Column(Float)
    risk_level = Column(String)

class Demographics(Base):
    __tablename__ = "demographics"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer)
    gender = Column(String)
    age_range = Column(String)
    education = Column(String)
    investment_experience = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
