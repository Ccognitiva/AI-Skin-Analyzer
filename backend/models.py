from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    skin_type = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

class SkinAnalysis(Base):
    __tablename__ = "skin_analysis"

    analysis_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    image_url = Column(Text)
    detected_conditions = Column(Text)
    analysis_date = Column(DateTime, default=datetime.utcnow)

class ProductRecommendation(Base):
    __tablename__ = "product_recommendations"

    recommendation_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    product_name = Column(String(255))
    confidence_score = Column(Float)
    recommended_at = Column(DateTime, default=datetime.utcnow)

class UserProgress(Base):
    __tablename__ = "user_progress"

    progress_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    analysis_id = Column(Integer, ForeignKey("skin_analysis.analysis_id"))
    skin_condition = Column(Text)
    improvement_score = Column(Float)
    tracked_at = Column(DateTime, default=datetime.utcnow)

class Consultation(Base):
    __tablename__ = "consultations"

    appointment_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    specialist_name = Column(String(100))
    appointment_date = Column(DateTime)
    status = Column(String(20), default="pending")
