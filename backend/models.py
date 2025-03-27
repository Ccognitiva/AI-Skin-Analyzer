from sqlalchemy import (
    Column, Integer, String, ForeignKey, Text, Float, DateTime, Table
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

# Association Table for Many-to-Many between SkinAnalysis and SkinCondition
skin_analysis_conditions = Table(
    "skin_analysis_conditions",
    Base.metadata,
    Column("analysis_id", Integer, ForeignKey("skin_analysis.analysis_id", ondelete="CASCADE"), primary_key=True),
    Column("condition_id", Integer, ForeignKey("skin_conditions.condition_id", ondelete="CASCADE"), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(Text, nullable=False)
    skin_type = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    analyses = relationship("SkinAnalysis", back_populates="user", cascade="all, delete-orphan")
    consultations = relationship("Consultation", back_populates="user", cascade="all, delete-orphan")
    progress = relationship("UserProgress", back_populates="user", cascade="all, delete-orphan")

class SkinCondition(Base):
    __tablename__ = "skin_conditions"

    condition_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    # Relationships
    recommended_products = relationship("ProductRecommendation", back_populates="skin_condition", cascade="all, delete-orphan")
    analyses = relationship("SkinAnalysis", secondary=skin_analysis_conditions, back_populates="detected_conditions")

class SkinAnalysis(Base):
    __tablename__ = "skin_analysis"

    analysis_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    image_url = Column(Text, nullable=False)
    analysis_date = Column(DateTime, server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="analyses")
    detected_conditions = relationship("SkinCondition", secondary=skin_analysis_conditions, back_populates="analyses")

class ProductRecommendation(Base):
    __tablename__ = "product_recommendations"

    recommendation_id = Column(Integer, primary_key=True, index=True)
    condition_id = Column(Integer, ForeignKey("skin_conditions.condition_id", ondelete="CASCADE"), nullable=False)
    product_name = Column(String(255), nullable=False)
    confidence_score = Column(Float, nullable=False)
    recommended_at = Column(DateTime, server_default=func.now())

    # Relationships
    skin_condition = relationship("SkinCondition", back_populates="recommended_products")

class UserProgress(Base):
    __tablename__ = "user_progress"

    progress_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    analysis_id = Column(Integer, ForeignKey("skin_analysis.analysis_id", ondelete="CASCADE"), nullable=False)
    skin_condition_id = Column(Integer, ForeignKey("skin_conditions.condition_id", ondelete="CASCADE"), nullable=False)
    improvement_score = Column(Float, nullable=False)
    tracked_at = Column(DateTime, server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="progress")
    skin_condition = relationship("SkinCondition")

class Consultation(Base):
    __tablename__ = "consultations"

    appointment_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    specialist_name = Column(String(100), nullable=False)
    appointment_date = Column(DateTime, nullable=False)
    status = Column(String(20), default="pending", nullable=False)

    # Relationships
    user = relationship("User", back_populates="consultations")
