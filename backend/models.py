from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

# Association Table for Many-to-Many between SkinAnalysis and SkinCondition
skin_analysis_conditions = Table(
    "skin_analysis_conditions",
    Base.metadata,
    Column("analysis_id", Integer, ForeignKey("skin_analysis.analysis_id"), primary_key=True),
    Column("condition_id", Integer, ForeignKey("skin_conditions.condition_id"), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    skin_type = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())

class SkinCondition(Base):
    __tablename__ = "skin_conditions"

    condition_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)

    # Relationship with Products
    recommended_products = relationship("ProductRecommendation", back_populates="skin_condition")

class SkinAnalysis(Base):
    __tablename__ = "skin_analysis"

    analysis_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    image_url = Column(Text)
    analysis_date = Column(DateTime, server_default=func.now())

    # Many-to-Many Relationship with SkinCondition
    detected_conditions = relationship("SkinCondition", secondary=skin_analysis_conditions, backref="analyses")

class ProductRecommendation(Base):
    __tablename__ = "product_recommendations"

    recommendation_id = Column(Integer, primary_key=True, index=True)
    condition_id = Column(Integer, ForeignKey("skin_conditions.condition_id"))
    product_name = Column(String(255))
    confidence_score = Column(Float)
    recommended_at = Column(DateTime, server_default=func.now())

    # Relationship with SkinCondition
    skin_condition = relationship("SkinCondition", back_populates="recommended_products")

class UserProgress(Base):
    __tablename__ = "user_progress"

    progress_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    analysis_id = Column(Integer, ForeignKey("skin_analysis.analysis_id"))
    skin_condition_id = Column(Integer, ForeignKey("skin_conditions.condition_id"))
    improvement_score = Column(Float)
    tracked_at = Column(DateTime, server_default=func.now())

    # Relationships
    skin_condition = relationship("SkinCondition")

class Consultation(Base):
    __tablename__ = "consultations"

    appointment_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    specialist_name = Column(String(100))
    appointment_date = Column(DateTime)
    status = Column(String(20), default="pending")
